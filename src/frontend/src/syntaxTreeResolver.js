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

export {
    travelTree,
    calcCodeMetricsValue
}