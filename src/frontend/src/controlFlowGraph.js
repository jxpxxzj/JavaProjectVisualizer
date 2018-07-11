var colorPad = ['#c23531','#2f4554', '#61a0a8', '#d48265', '#91c7ae','#749f83',  '#ca8622', '#bda29a','#6e7074', '#546570', '#c4ccd3']
var colorDict = {
    'entry': colorPad[1],
    'IfStatement': colorPad[2],
    'ForStatement': colorPad[3],
    'WhileStatement': colorPad[3],
    'DoWhileStatement': colorPad[3],
    'ReturnStatement': colorPad[4],

    'trueBranch': colorPad[5],
    'falseBranch': colorPad[6]
}

var symbolDict = {
    'entry': 'pin',
    'IfStatement': 'diamond',
    'ForStatement': 'diamond',
    'WhileStatement': 'diamond',
    'DoWhileStatement': 'diamond',
    'ReturnStatement': 'rectangle'
}

function getStatementList(syntaxTree, methodSignature) {
    if (syntaxTree == undefined) {
        return []
    }

    var list = []
    var currentId = 0

    function travel(tree) {
        var obj = {
            node: tree,
            id: currentId++,
            next: []
        };

        list.push(obj)

        var children = tree.children

        if (tree.type == 'IfStatement') { // maybe two branches
            var hasFalseBranch = children.length == 2 // if has falseBranch
            var trueBranch = children[0].children // should be IfTrueBranch's statements
            var falseBranch = hasFalseBranch ? children[1].children : undefined // should be IfFalseBranch's statements
            trueBranch.forEach(t => {
                travel(t);
            });
            if (hasFalseBranch) {
                falseBranch.forEach(t => {
                    travel(t);
                })
            }
        }
        
        if (tree.type == 'ForStatement' || tree.type == 'WhileStatement' || tree.type == 'DoWhileStatement') { // loop statements
            for(let i=0; i<children.length; i++) {
                travel(children[i])
            }
        }

        return obj
    }
    //            file       package     class       methods
    var methods = syntaxTree.children[0].children[0].children
    var method = methods.find(t => t.signature == methodSignature)
    method.children.forEach(element => {
        travel(element);
    });

    return list.flat().sort((a,b) => a.id - b.id);
}

function calcLinkList(syntaxTree, methodSignature) {
    var statements = getStatementList(syntaxTree, methodSignature)

    function getRootStatement() {
        var list = []
        var methods = syntaxTree.children[0].children[0].children
        var method = methods.find(t => t.signature == methodSignature)
        for(var i=0;i<statements.length;i++) {
            if (method.children.includes(statements[i].node)) {
                list.push(statements[i])
            }
        }
        return list
    }

    var rootStatements = getRootStatement()

    function findStatement(node) {
        return statements.find(t => t.node == node)
    }

    function getBranchParent(branchNode) {
        function travel(tree, node) {
            if (tree.children.includes(node)) {
                return tree
            } else { // search children branch
                for(var i=0;i<tree.children.length;i++) {
                    var result = travel(tree.children[i], node)
                    if (result) {
                        return result
                    }
                }
            }
        }

        return travel(syntaxTree, branchNode)
    }

    function findParentStatement(statement) {
        function travel(tree, node) {
            if (tree.children.includes(node)) {
                return tree;
            } else {
                var result = null;
                for(var i=0;i<tree.children.length;i++) {
                    var t = tree.children[i]
                    result = travel(t, node)
                    if (result) {
                        return result 
                    }
                }
            }
        }
        var result = travel(syntaxTree, statement.node)
        if (result) {
            if (result.type == 'IfTrueBranch' || result.type == 'IfFalseBranch') {
                result = getBranchParent(result)
            }
            return findStatement(result)
        }
    }
    
    function getNextStatement(statement) {
        var next = []

        if (statement.node.type == 'IfStatement') { // if statements may have two branches
            var hasFalseBranch = statement.node.children.length == 2
            var trueBranch = statement.node.children[0] // should be IfTrueBranch
            var falseBranch = hasFalseBranch ? statement.node.children[1] : undefined // should be IfFalseBranch
            next.push(findStatement(trueBranch.children[0])) // push first statement of true branch
            if (hasFalseBranch) {
                next.push(findStatement(falseBranch.children[0])) // push first statement of false branch
                // return next // do not continue since only two next is allowed
            } // else: just simply skip this if statement
        }

        if (statement.node.type == 'DoWhileStatement') { 
            next.push(findStatement(statement.node.children[0])) // goto the first statement of do..while
        }

        if (statement.node.type == 'ForStatement' || statement.node.type == 'WhileStatement') {
            next.push(findStatement(statement.node.children[0])) // first statement of block
        } // else: continue to handle skip

        if (findStatement(statement.node) != rootStatements[rootStatements.length - 1]) { // is not the last statement of method
            var parent = findParentStatement(statement)
            if (parent != undefined) { // is in a code block
                var parentChildren = parent.node.children
                var index = parentChildren.indexOf(statement.node);
                if (parent.node.type == 'IfStatement') {
                    var hasFalseBranch = parent.node.children.length == 2
                    parentChildren = parent.node.children[0].children // TrueBranch's children
                    index = parentChildren.indexOf(statement.node)
                    if (index == -1 && hasFalseBranch) {
                        parentChildren = parent.node.children[1].children // FalseBranch's children
                        index = parentChildren.indexOf(statement.node)
                    }
                }

                if (index == parentChildren.length - 1) { // is the last statement of this block
                    if (parent.node.type == 'DoWhileStatement') {
                        next = [findStatement(parent.node)]
                    } else if (parent.node.type == 'ForStatement' || parent.node.type == 'WhileStatement') { // for statement and while statement should return to its start
                        next.push(parent) // return to parent's parameter
                    } else if (parent.node.type == 'IfStatement') {
                        var nextStatements = getNextStatement(parent)
                        next.push(nextStatements[nextStatements.length - 1]) // the last element will exit that if statement
                    } else {
                        next.push(getNextStatement(parent)); // get parent's next statement
                    }
                } else { // is in the mid of parents
                    next.push(findStatement(parentChildren[index + 1])); // return its next
                    // handle do..while
                    for(var i=0;i<next.length;i++) {
                        if (next[i].node != undefined && next[i].node.type == 'DoWhileStatement') {
                            next[i] = findStatement(next[i].node.children[0])
                        }
                    }
                }
            } else { // method scope
                var index = rootStatements.indexOf(statement)
                next.push(rootStatements[index + 1]); // return next statement
                // handle do..while
                for(var i=0;i<next.length;i++) {
                    if (next[i].node != undefined && next[i].node.type == 'DoWhileStatement') {
                        next[i] = findStatement(next[i].node.children[0])
                    }
                }
            }
        } else {// else: there is no statements
            next.push(-1)
        }

        return next
    }

    var linkList = []
    statements.forEach(t => {
        linkList.push(getNextStatement(t).flat());
    })
    linkList = linkList.map(t => t.map(u => u.id+1).slice(0, 2))
    
    return linkList
}

function getNode(statement, firstOrLast=false, name='', value='') {
    var node = {
        itemStyle: {
            color: colorPad[0]
        }
    }

    if (firstOrLast) {
        node.itemStyle.color = colorDict['entry']
        node.symbol = symbolDict['entry']
        node.name = name
        node.value = value
        return node
    }

    if (colorDict[statement.node.type] != undefined) {
        node.itemStyle.color = colorDict[statement.node.type];
    }
    
    if (symbolDict[statement.node.type] != undefined) {
        node.symbol = symbolDict[statement.node.type];
    }

    function getNodeLabel(syntaxNode) {
        var str = ''
        if (syntaxNode.type == 'IfStatement') {
            str = `if (${syntaxNode.condition})`
        }
        
        if (syntaxNode.type == 'VariableDeclarator') {
            str = `${syntaxNode.valueType} ${syntaxNode.left} = ${syntaxNode.right}`
        }

        if (syntaxNode.type == 'ForStatement') {
            str = `for (${syntaxNode.condition})`
        }

        if (syntaxNode.type == 'WhileStatement' || syntaxNode.type == 'DoWhileStatement') {
            str = `while (${syntaxNode.condition})`
        }

        if (syntaxNode.type == 'AssignStatement') {
            str = `${syntaxNode.left} ${syntaxNode.op} ${syntaxNode.right}`
        }

        if (syntaxNode.type == 'MethodCallStatement') {
            str = `${syntaxNode.name}(${syntaxNode.expressionList == null ? '' : syntaxNode.expressionList})`
        }

        if (syntaxNode.type == 'ReturnStatement') {
            str = `return ${syntaxNode.expression}`
        }

        return str
    }

    node.name = getNodeLabel(statement.node)
    node.value = `${statement.node.type} @ ${statement.node.start == statement.node.stop ? statement.node.start : statement.node.start + ' ~ ' + statement.node.stop}`

    return node
}

function getLink(linkList, statements, endIndex) {
    var links = []
    var initTargetId = 1
    for(var i=0;i<statements.length;i++) {
        if (statements[i].node.type == 'DoWhileStatement') {
            initTargetId++;
        } else {
            break;
        }
    }
    links.push({
        source: 0,
        target: initTargetId
    })
    for(var i=0;i<linkList.length;i++) {
        if (statements[i].node.type == 'ReturnStatement') {
            links.push({
                source: i+1,
                target: endIndex
            })
            continue;
        }

        if (linkList[i].length == 0) {
            links.push({
                source: i+1,
                target: endIndex
            })
        }

        if (linkList[i].length == 1) {
            var isEnd = isNaN(linkList[i][0])
            var value = linkList[i][0]
            if (isEnd) {
                value = endIndex
            }
            links.push({
                source: i+1,
                target: value
            })
        }

        if (linkList[i].length == 2) {
            links.push({
                source: i+1,
                target: linkList[i][0],
                label: {
                    show: true,
                    formatter: 'True'
                }
            })
            var isEnd = isNaN(linkList[i][1])
            var value = linkList[i][1]
            if (isEnd) {
                value = endIndex
            }
            links.push({
                source: i+1,
                target: value,
                label: {
                    show: true,
                    formatter: 'False'
                }
            })
        }
    }
    return links
}

function getFlow(syntaxTree, methodSignature) {
    var linkList = calcLinkList(syntaxTree, methodSignature)
    var statements = getStatementList(syntaxTree, methodSignature)

    var methods = syntaxTree.children[0].children[0].children
    var method = methods.find(t => t.signature == methodSignature)

    var statementsNodes = [getNode(undefined, true, methodSignature, `${method.type} @ ${method.start} ~ ${method.stop}`)]
    statementsNodes = statementsNodes.concat(statements.map(t => getNode(t)))
    statementsNodes.push(getNode(undefined, true, 'End')) 

    function processDuplicateName(statementsNodes) {
        var dict = {}
        for(var i=0;i<statementsNodes.length;i++) {
            var node = statementsNodes[i]
            if (dict[node.name] != undefined) {
                node.name += `~${dict[node.name]}`
                dict[node.name]++
            } else {
                dict[node.name] = 0
            }
        }
    }

    processDuplicateName(statementsNodes)

    var links = getLink(linkList, statements, statementsNodes.length-1)
    return {
        data: statementsNodes,
        links
    }
}

export {
    getFlow
}