function elemBase() {}
elemBase.prototype.toString = function() {
    return this.fullName;
}

function travelTree(sytnaxTree) {
    var obj = {
      
    }

    function travel(tree) {
        if (obj[tree.type] == undefined) {
            obj[tree.type] = []
        }

        var elem = new elemBase();
        elem.start = tree.start
        elem.stop = tree.stop
        elem.nodeType = tree.type

        var str = tree.name;
        if (tree.type == 'Annotation') {
            str = `@${str}`
        }     
        elem.name = str;

        var qualifiedName = ''
        if (tree.packageName) {
            qualifiedName += tree.packageName
        }
        if (tree.className) {
            if (qualifiedName != '') {
                qualifiedName += '.'
            }
            qualifiedName += tree.className
        }
        elem.qualifiedScope = qualifiedName
        if (qualifiedName != '') {
            qualifiedName += '::'
        }
        
        str = `${qualifiedName}${str}`

        if (tree.type == 'Field') {
            str = `${tree.valueType} ${str}`; 
            elem.type = tree.valueType;
        }
        
        if (tree.type == 'Method' || tree.type == 'InterfaceMethod' || tree.type == 'AnnotationTypeElement' || tree.type == 'Constructor') {
            var params = ''
            elem.signature = tree.signature;
            if (tree.parameters)
                var params = tree.parameters.join(', ')
                elem.params = params
                elem.methodBody = tree.children
            if (tree.type != 'Constructor') {
                str = `${tree.returnType} ${str}(${params})`
                elem.type = tree.returnType
            } else {
                str = `${str}(${params})`
            }
        }
        
        elem.fullName = str;

        obj[tree.type].push(elem);
        tree.children.forEach(element => {
            travel(element)
        });
    }

    travel(sytnaxTree)
    return obj
}

function calcCodeMetricsValue(methodBody) {
    var obj = {
        cyclomaticComplexity: 1,
        classCoupling: 0
    }

    var valueTypeList = {}

    function countInstances(string, word) {
        return string.split(word).length - 1;
     }

    function travel(tree) {
        if (tree.valueType != undefined) {
            valueTypeList[tree.valueType] = true
        }
        if (tree.condition != undefined) { // is do..while / while / if
            obj.cyclomaticComplexity++;
            obj.cyclomaticComplexity += countInstances(tree.condition, '&&')
            obj.cyclomaticComplexity += countInstances(tree.condition, '||')
        }
        tree.children.forEach(element => {
            travel(element)
        });
    }

    methodBody.forEach(element => {
        travel(element)
    });

    obj.classCoupling = Object.keys(valueTypeList).length

    return obj;
}

function toViewTree(syntaxTree, methodSignature) {
    // create a deep copy of syntaxTree
    var newTree = JSON.parse(JSON.stringify(syntaxTree))

    var methods = newTree.children[0].children[0].children
    var method = methods.find(t => t.signature == methodSignature)

    function travel(tree) {
        tree.title = `${tree.name == undefined || tree.type == tree.name ? '' : ':' + tree.name} @ ${tree.start == tree.stop ? tree.start : tree.start + ' ~ ' + tree.stop}`
        tree.expand = false
        tree.render = function(h, {root, node, data}) {
            return h('span', {
                style: {
                    display: 'inline-block',
                    width: '100%'
                }
            }, [
                    h(('span'), {
                        style: {
                            fontWeight: 'bold'
                        }
                    }, data.type),
                    h(('span'), data.title)
            ]);
        }
        tree.children.forEach(element => {
            travel(element)
        });
    }

    travel(method)
    return method
}

export {
    travelTree,
    calcCodeMetricsValue,
    toViewTree
}