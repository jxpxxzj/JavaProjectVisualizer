
function travelTree(sytnaxTree) {
    var obj = {
      
    }

    function elemBase() {}
    elemBase.prototype.toString = function() {
        return this.fullName;
    }
    
    function travel(tree) {
        if (obj[tree.type] == undefined) {
            obj[tree.type] = []
        }

        var elem = new elemBase();

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
            if (tree.parameters)
                var params = tree.parameters.join(', ')
                elem.params = params
            if (tree.type != 'Constructor') {
                str = `${tree.returnType} ${str}(${params})`
                elem.type = tree.returnType
            } else {
                str = `${str}(${params})`
            }
        }
        
        elem.fullName = str;

        obj[tree.type].push(elem)
        tree.children.forEach(element => {
            travel(element)
        });
    }

    travel(sytnaxTree)
    return obj
}

export {
    travelTree
}