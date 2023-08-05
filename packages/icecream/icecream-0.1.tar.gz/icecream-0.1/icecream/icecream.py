#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# IceCream - A little library for sweet and creamy print debugging.
#
# Ansgar Grunseid
# grunseid.com
# grunseid@gmail.com
#
# License: MIT
#

import ast
import dis
import inspect
import textwrap
from os.path import basename


MYNAME = 'ic'
PREFIX = '%s| ' % MYNAME


# TODO(grun): Allow for configuration of output. Support output not just to
# stdout, but other places, too (logging, custom function, etc). Also add
# support for the output of additional fields, like timestamps.
def configureOutput():
    raise NotImplementedError


def classname(obj):
    return obj.__class__.__name__


def printOut(s, inludeTimestamp=False):
    print(''.join([PREFIX, s]))


def splitStringAtIndices(s, indices):
    return [s[i:j] for i, j in zip([0] + indices, indices + [None]) if s[i:j]]


def calcuateLineOffsets(code):
    return dict((line, offset) for offset, line in dis.findlinestarts(code))


def getCallSourceLines(funcName, callFrame):
    code = callFrame.f_code
    parentBlockStartLine = code.co_firstlineno
    parentBlockSource = inspect.getsource(code)

    lineno = inspect.getframeinfo(callFrame)[1]
    linenoRelativeToParent = lineno - parentBlockStartLine + 1

    # There could be multiple ic() calls on the same line(s), like
    #
    #   ic(1); ic(2); ic(3,
    #       4,
    #       5); ic(6)
    #
    # so include all of them. Which invocation is the appropriate one will be
    # determined later via bytecode offset calculations.
    #
    # TODO(grun): Support invocations of ic() where ic() is an attribute chain
    # in the AST. For example, support
    #
    #   import icecream
    #   icecream.ic()
    #
    # and
    #
    #   class foo():
    #     blah = ic
    #   foo.ic()
    #
    parentBlockSource = textwrap.dedent(parentBlockSource)
    potentialCalls = [
        node for node in ast.walk(ast.parse(parentBlockSource))
        if classname(node) == 'Call' and classname(node.func) == 'Name' and
        node.func.id == funcName and (
            node.lineno == linenoRelativeToParent or
            any(arg.lineno == linenoRelativeToParent for arg in node.args))]

    endLine = lineno - parentBlockStartLine + 1
    startLine = min(call.lineno for call in potentialCalls)
    lines = parentBlockSource.splitlines()[startLine - 1 : endLine]
    source = ' '.join(line.strip() for line in lines)

    callOffset = callFrame.f_lasti
    absoluteStartLineNum = parentBlockStartLine + startLine - 1
    startLineOffset = calcuateLineOffsets(code)[absoluteStartLineNum]

    return source, absoluteStartLineNum, startLineOffset

def splitExpressionsOntoSeparateLines(source):
    """
    Split every expression onto its own line so any preceeding and/or trailing

    expressions, like foo(1) and foo(2) of

      foo(1); ic(1); foo(2)

    are properly separated from ic(1) for dis.findlinestarts(). Otherwise,
    preceeding and trailer expressions, like foo(1) and foo(2) above, break the
    calculation of ic(1)'s the bytecode offsets with dis.findlinestarts().
    """
    indices = [expr.col_offset for expr in ast.parse(source).body]
    lines = [s.rstrip(' ;') for s in splitStringAtIndices(source, indices)]
    oneExpressionPerLine = '\n'.join(lines)

    return oneExpressionPerLine


def splitCallsOntoSeparateLines(funcName, source):
    """
    To determine the bytecode offsets of ic() calls with dis.findlinestarts(),
    every ic() invocation needs to start its own line. That is, this
    
      foo(ic(1), ic(2))
    
    needs to be turned into
    
      foo(
      ic(1),
      ic(2))
    
    Then the bytecode offsets of ic(1) and ic(2) can be determined with
    dis.findlinestarts().

    This split is necessary for ic() calls inside other expressions,
    like foo(ic(1)), to be extracted correctly.
    """
    callIndices = [
        node.func.col_offset for node in ast.walk(ast.parse(source))
        if classname(node) == 'Call' and node.func.id == funcName]
    toks = splitStringAtIndices(source, callIndices)
    sourceWithNewlinesBeforeInvocations = '\n'.join(toks)

    return sourceWithNewlinesBeforeInvocations


def extractCallStrByOffset(splitSource, callOffset):
    code = compile(splitSource, '<string>', 'exec')
    lineOffsets = sorted(calcuateLineOffsets(code).items())

    # For lines with multiple invocations, like 'ic(1); ic(2)', determine which
    # invocation was called.
    for lineno, offset in lineOffsets:
        if callOffset >= offset:
            sourceLineIndex = lineno - 1
        else:
            break

    lines = [s.rstrip(' ;') for s in splitSource.splitlines()]
    line = lines[sourceLineIndex]

    # Find the ic() call's matching right parenthesis. This is necessary
    # whenever there are closing tokens (e.g. ')', ']', '}', etc) after the
    # ic() call. Like
    #
    #   foo(
    #     foo(
    #       {
    #         ic(
    #           bar())}))
    #
    # where the <line> 'ic(bar())}))' needs to be trimmed to just 'ic(foo())'.
    # Unfortunately, afaik there's no way to determine the character width of a
    # function call, or its last argument, from the AST, so a workaround is to
    # truncate right parens (and any non-right-paren junk thereafter) from
    # <line> until ic()'s matching right paren is found. Bit of a hack, but
    # ¯\_(ツ)_/¯.
    line = line[:line.rfind(')') + 1]  # Remove everything after the last ')'.
    while True:
        try:
            ast.parse(line)  # Mismatched parens raises SyntaxError.
            break
        except SyntaxError:
            rightmostClosingParen = line.rfind(')')
            line = line[:line.rfind(')', 0, rightmostClosingParen) + 1]

    callStr = line
    return callStr


def extractArgumentsFromCallStr(callStr):
    """
    Parse the argument string via an AST instead of the overly simple
    callStr.split(','). The latter incorrectly splits any string parameters
    that contain commas therein, like ic(1, 'a,b', 2).
    """
    params = callStr.split('(', 1)[-1].rsplit(')', 1)[0].strip()

    body = ast.parse(params).body[0]
    eles = body.value.elts if classname(body.value) == 'Tuple' else [body.value]

    indices = [ele.col_offset for ele in eles]
    argStrs = [s.strip(' ,') for s in splitStringAtIndices(params, indices)]

    return argStrs


def icWithoutArgs(callFrame, funcName):
    # For multiline invocations, like
    #
    #   ic(
    #      )
    #
    # report the call start line, not the call ending line. I.e. report the
    # line number of 'ic(' in the example above, not ')'. Unfortunately the
    # readily available <frameInfo.lineno> is the end line, not the start line,
    # so it can't be used.
    _, startLine, _ = getCallSourceLines(funcName, callFrame)

    frameInfo = inspect.getframeinfo(callFrame)
    filename = basename(frameInfo.filename)

    out = '%s:%s' % (filename, startLine)
    printOut(out)


def icWithArgs(callFrame, funcName, args):
    callSource, _, callSourceOffset = getCallSourceLines(funcName, callFrame)

    callOffset = callFrame.f_lasti
    relativeCallOffset = callOffset - callSourceOffset

    # Insert newlines before every expression and every ic() call so a mapping
    # between col_offsets (in characters) and f_lastis (in bytecode) can be
    # determined with dis.findlinestarts().
    oneExpressionPerLine = splitExpressionsOntoSeparateLines(callSource)
    splitSource = splitCallsOntoSeparateLines(funcName, oneExpressionPerLine)

    callStr = extractCallStrByOffset(splitSource, relativeCallOffset)
    argStrs = extractArgumentsFromCallStr(callStr)

    pairs = list(zip(argStrs, args))

    output = ', '.join('%s: %r' % (arg, value) for arg, value in pairs)
    printOut(output)


def ic(*args):
    # TODO(grun): Determine the function name dynamically to account for
    # renaming. For example, this function's name can be different if it was
    # imported under a different name, like
    #
    #   from ic import ic as newname
    #
    # Or simply renamed
    #
    #   from ic import ic
    #   newname = ic
    #   newname('blah')
    #
    # Account for both scenarios.
    funcName = inspect.stack()[0][3]
    callFrame = inspect.currentframe().f_back

    if not args:
        icWithoutArgs(callFrame, funcName)
    else:
        icWithArgs(callFrame, funcName, args)
