<template>
    <div class="w-container">
        <Row>
            <Upload action="/api/upload" :before-upload="onBeforeUpload" :on-success="onUploadSuccess" :show-upload-list="false">
                <Button type="ghost" icon="ios-cloud-upload-outline">Upload file</Button>
                <span v-if="fileKey == null" style="margin-left: 10px">Upload a zip file to start analyze.</span>
                <span v-if="fileKey != null" style="margin-left: 10px">File Key: {{ fileKey }} </span>
            </Upload>
        </Row>
        <Row v-if="treeResolverValue != null">
            <Tabs value="glob" style="height: 100%">
                <TabPane label="Project View" name="glob">
                    <Row>
                        <iCol :span="5">
                            <Menu active-name="1" @on-select="onMenuChange">
                                <MenuItem name="1">
                                   Overview
                                </MenuItem>
                                <MenuItem name="2">
                                    Package and Class Diagram
                                </MenuItem>
                                <MenuItem name="3">
                                    Line of Codes ({{this.syntaxTree.value}})
                                </MenuItem>
                            </Menu>
                        </iCol>
                        <iCol :span="19">
                            <div v-show='activeMenu == "1"' class='menu-page' style="margin-bottom: 20px">
                                <Tabs value="package" style="height: 100%">
                                    <TabPane v-if="treeResolverValue.Package != undefined" :label="`Package (${treeResolverValue.Package.length})`" name="package">
                                        <Table border height="550" :columns="tableCols.package" :data="treeResolverValue.Package"></Table>
                                    </TabPane>
                                    <TabPane v-if="treeResolverValue.Class != undefined" :label="`Class (${treeResolverValue.Class.length})`" name="class">
                                        <Table border height="550" :columns="tableCols.class" :data="treeResolverValue.Class"></Table>
                                    </TabPane>
                                    <TabPane v-if="treeResolverValue.Constructor != undefined" :label="`Constructor (${treeResolverValue.Constructor.length})`" name="constructor">
                                        <Table border height="550" :columns="tableCols.constructor" :data="treeResolverValue.Constructor"></Table>
                                    </TabPane>
                                    <TabPane v-if="treeResolverValue.Method != undefined" :label="`Method (${treeResolverValue.Method.length})`" name="method">
                                        <Table border height="550" :columns="tableCols.method" :data="treeResolverValue.Method"></Table>
                                    </TabPane>
                                    <TabPane v-if="treeResolverValue.Field != undefined" :label="`Field (${treeResolverValue.Field.length})`" name="field">
                                        <Table border height="550" :columns="tableCols.field" :data="treeResolverValue.Field"></Table>
                                    </TabPane>
                                    <TabPane v-if="treeResolverValue.Interface != undefined" :label="`Interface (${treeResolverValue.Interface.length})`" name="interface">
                                        <Table border height="550" :columns="tableCols.interface" :data="treeResolverValue.Interface"></Table>
                                    </TabPane>
                                    <TabPane v-if="treeResolverValue.InterfaceMethod != undefined" :label="`Interface Method (${treeResolverValue.InterfaceMethod.length})`" name="interfaceMethod">
                                        <Table border height="550" :columns="tableCols.interfaceMethod" :data="treeResolverValue.InterfaceMethod"></Table>
                                    </TabPane>
                                    <TabPane v-if="treeResolverValue.Annotation != undefined" :label="`Annotation (${treeResolverValue.Annotation.length})`" name="annotation">
                                        <Table border height="550" :columns="tableCols.annotation" :data="treeResolverValue.Annotation"></Table>
                                    </TabPane>
                                    <TabPane v-if="treeResolverValue.AnnotationTypeElement != undefined" :label="`Annotation Method (${treeResolverValue.AnnotationTypeElement.length})`" name="annotationTypeElement">
                                        <Table border height="550" :columns="tableCols.annotationTypeElement" :data="treeResolverValue.AnnotationTypeElement"></Table>
                                    </TabPane>
                                </Tabs>
                            </div>
                            <div v-show='activeMenu == "2"' class='menu-page'>
                                <chart :options="tree" style="width: 1200px; height: 600px"></chart>
                            </div>
                            <div v-show='activeMenu == "3"' class='menu-page'>
                                <chart :options="treeMap" style="width: 1200px; height: 600px"></chart>
                            </div>
                        </iCol>
                    </Row>
                </TabPane>
                <TabPane label="Source code browser" name="file">
                    <Row :gutter="20">
                        <Spin size="large" fix v-if="browserSpinShow"></Spin>
                        <iCol :span="6">
                            <Tree :data="fileTree" @on-select-change="onTreeSelectChange"></Tree>
                        </iCol>
                        <iCol :span="18" v-if="code != ''">
                            <Row v-if="fileSyntaxTreeResolverValue.Method != undefined && fileSyntaxTreeResolverValue.Method.length > 0">
                                <Select v-model="memberSelected" @on-change="onSelectChange">
                                    <Option value="sourceCode">Source Code</Option>
                                    <Option v-for="(item,index) in fileSyntaxTreeResolverValue.Method" :value="item.signature" :key="index">{{ item.signature }}</Option>
                                </Select>
                            </Row>
                            <Row :gutter="20">
                                <div v-if="memberSelected == 'sourceCode'">
                                    <pre v-highlightjs="code"><code class="x-java"></code></pre>
                                </div>
                                <div v-else>
                                    <iCol :span="12">
                                        <pre v-highlightjs="code"><code class="x-java"></code></pre>
                                    </iCol>
                                    <iCol :span="12">
                                        <div style="margin-top: 12px;">
                                            <Tabs>
                                                <TabPane label="Syntax Tree">
                                                    <Tree :data="sourceBrowserViewTree"></Tree>
                                                </TabPane>
                                                <TabPane label="Control Flow Graph">
                                                    <chart :options="flowGraph" style="width: 500px; height: 500px"></chart>
                                                    <Modal v-model="graphFullscreen" title="Control Flow Graph" :mask-closable="false" 
                                                        cancel-text="" ok-text="Close" width="1200" @on-ok="toggleFullscreen" @on-cancel="toggleFullscreen">                                                                     
                                                        <chart :options="flowGraph" style="width: 1150px; height: 550px"></chart>
                                                    </Modal>
                                                    <Button type="primary" @click="toggleFullscreen">Fullscreen</Button>
                                                </TabPane>
                                                <TabPane label="Metrics Value">
                                                    <Table border :columns="sourceBrowserTableCols" :data="sourceBrowserTableValue"></Table>
                                                </TabPane>
                                            </Tabs>
                                        </div>
                                    </iCol>
                                </div>
                            </Row>
                        </iCol>
                    </Row>
                </TabPane>
            </Tabs>
        </Row>
    </div>
</template>
<style>
html, body {
    height: 100%;
}
.menu-page {
    width: 100%;
}
.w-container {
    height: 100%;
    margin-top: 20px;
    margin-left: 20px;
    margin-right: 20px;
}
.ivu-tree {
    user-select: none;
}
td.hljs-ln-numbers {
    user-select: none;
    text-align: center;
    color: #ccc;
    border-right: 1px solid #CCC;
    vertical-align: top;
    padding-right: 5px !important;
}
td.hljs-ln-code {
    padding-left: 10px !important; 
}

</style>
<script>
import { travelTree, calcCodeMetricsValue, toViewTree } from './syntaxTreeResolver'
import { getFlow } from './controlFlowGraph'

function colorMappingChange(value) {
    var levelOption = getLevelOption(value);
    chart.setOption({
        series: [{
            levels: levelOption
        }]
    });
}

function getLevelOption() {
    return [
        {
            itemStyle: {
                normal: {
                    borderColor: '#777',
                    borderWidth: 0,
                    gapWidth: 1
                }
            },
            upperLabel: {
                normal: {
                    show: false
                }
            }
        },
        {
            itemStyle: {
                normal: {
                    borderColor: '#555',
                    borderWidth: 5,
                    gapWidth: 1
                },
                emphasis: {
                    borderColor: '#ddd'
                }
            }
        },
        {
            colorSaturation: [0.35, 0.5],
            itemStyle: {
                normal: {
                    borderWidth: 5,
                    gapWidth: 1,
                    borderColorSaturation: 0.6
                }
            }
        }
    ];
}

var colsIorCorA = [
    {
        title: 'Qualified Scope',
        key: 'qualifiedScope'
    }, {
        title: 'Name',
        key: 'name'
    }
]

var paramsRender = (h, params) => {
    return h('div', params.row.params.split(', ').map(t => h('p', t)));
}

var colsMorIMorATE = [
    {
        title: 'Qualified Scope',
        key: 'qualifiedScope'
    }, {
        title: 'Name',
        key: 'name'
    }, {
        title: 'Parameter List',
        key: 'params',
        render: paramsRender
    }, {
        title: 'Returns type',
        key: 'type'
    }
]

var colsF = [
    {
        title: 'Qualified Scope',
        key: 'qualifiedScope'
    }, {
        title: 'Name',
        key: 'name'
    }, {
        title: 'Type',
        key: 'type'
    }
]

var colsC = [
    {
        title: 'Qualified Scope',
        key: 'qualifiedScope'
    }, {
        title: 'Parameter List',
        key: 'params',
        render: paramsRender
    }
]

var colsP = [
    {
        title: 'Name',
        key: 'name'
    }
]

var colMV = [
    {
        title: 'Key',
        key: 'key'
    },
    {
        title: 'Value',
        key: 'value'
    }
]

export default {
    name: 'app',
    data () {
        return {
            browserSpinShow: false,
            treeResolverValue: null,
            tableCols: {
                package: colsP,
                class: colsIorCorA,
                constructor: colsC,
                method: colsMorIMorATE,
                field: colsF,
                interface: colsIorCorA, 
                interfaceMethod: colsMorIMorATE,
                annotation: colsIorCorA,
                annotationTypeElement: colsMorIMorATE
            },
            sourceBrowserTableCols: colMV,
            sourceBrowserTableValue: [],
            sourceBrowserViewTree: [],
            activeMenu: '1',
            syntaxTree: {
                children: []
            },
            tree: {
                tooltip: {
                    trigger: 'item',
                    triggerOn: 'mousemove'
                },
                series: [
                    {
                        type: 'tree',
                        data: [],
                        top: '1%',
                        left: '7%',
                        bottom: '1%',
                        right: '20%',
                        symbolSize: 7,
                        label: {
                            normal: {
                                position: 'left',
                                verticalAlign: 'middle',
                                align: 'right',
                                fontSize: 9
                            }
                        },
                        leaves: {
                            label: {
                                normal: {
                                    position: 'right',
                                    verticalAlign: 'middle',
                                    align: 'left'
                                }
                            }
                        },
                        expandAndCollapse: true,
                        animationDuration: 550,
                        animationDurationUpdate: 750
                    }
                ]
            },
            treeMap: {
                tooltip: {
                    formatter: function (info) {
                        var value = info.value;
                        var treePathInfo = info.treePathInfo;
                        var treePath = [];  
                        for (var i = 1; i < treePathInfo.length; i++) {
                            treePath.push(treePathInfo[i].name);
                        }   
                        return [
                            '<div class="tooltip-title">' + treePath.join('/') + '</div>',
                            'Line of codes: ' + value,
                        ].join('');
                    }
                },  
                series: [
                    {
                        name:'Line of codes',
                        type:'treemap',
                        visibleMin: 500,
                        zoomToNodeRatio: 0.381924,
                        leafDepth: 2,
                        label: {
                            show: true,
                            formatter: '{b}'
                        },
                        upperLabel: {
                            normal: {
                                show: true,
                                height: 30
                            }
                        },
                        itemStyle: {
                            normal: {
                                borderColor: '#fff'
                            }
                        },
                        levels: getLevelOption(),
                        data: []
                    }
                ]  
            },
            flowGraph: {
                tooltip: {
                    formatter: '{b}<br>{c}'
                },
                animationDurationUpdate: 1500,
                animationEasingUpdate: 'quinticInOut',
                series : [
                    {
                        type: 'graph',
                        symbolSize: 50,
                        roam: true,
                        label: {
                            normal: {
                                show: true
                            }
                        },
                        edgeSymbol: ['circle', 'arrow'],
                        edgeSymbolSize: [4, 10],
                        edgeLabel: {
                            normal: {
                                textStyle: {
                                    fontSize: 20
                                }
                            }
                        },
                        layout: 'force',
                        force: {
                            repulsion: 2000,
                            gravity: 0.01,
                        },
                        data: [],
                        links: [],
                        lineStyle: {
                            normal: {
                                opacity: 0.9,
                                width: 2,
                                curveness: 0.1
                            }
                        }
                    }
                ]
            },
            memberSelected: 'sourceCode',
            fileSyntaxTree: {
                children: []
            },
            fileSyntaxTreeResolverValue: {
                Method: []
            },
            code: '',
            fullCode: '',
            fileKey: null,
            fileTree: [],
            graphFullscreen: false
        }
    },
    methods: {
        toggleFullscreen() {
            this.graphFullscreen = !this.graphFullscreen;
        },
        onBeforeUpload() {
            this.$Spin.show();
            return true;
        },
        onMenuChange(name) {
            this.activeMenu = name
        },
        onSelectChange(value) {
            this.graphFullscreen = false
            if (value == 'sourceCode') {
                this.code = this.fullCode;
            } else {
                var currentMethod = this.fileSyntaxTreeResolverValue.Method.find(t => t.signature == value);
                var codeList = this.fullCode.split('\n').slice(currentMethod.start-1, currentMethod.stop)
                var mIndent = codeList[0].length - codeList[0].trimLeft().length
                var finalCode = codeList.map(t => t.slice(mIndent)).join('\n')
                var flow = getFlow(this.fileSyntaxTree, value)
                this.flowGraph.series[0].data = flow.data
                this.flowGraph.series[0].links = flow.links
                this.sourceBrowserViewTree = [toViewTree(this.fileSyntaxTree, value)]

                var metricsValue = calcCodeMetricsValue(currentMethod.methodBody);
                
                this.sourceBrowserTableValue = [
                    {
                        'key': 'Line of codes',
                        'value': currentMethod.stop - currentMethod.start + 1
                    }, {
                        'key': "McCabe's Cyclomatic Complexity",
                        'value': metricsValue.cyclomaticComplexity
                    }, {
                        'key': 'Class Coupling',
                        'value': metricsValue.classCoupling
                    }
                ]
                
                this.code = finalCode;
            }
            var that = this;
            var timeoutFunc = function() {
                if (window.hljs.initLineNumbersOnLoad != undefined) {
                    that.$nextTick(function() {
                        window.hljs.initLineNumbersOnLoad();
                    })
                }
                var codeElement = document.querySelector('code');
                if (codeElement) {
                    var html = codeElement.innerHTML
                    if (!html.includes('<table>')) {
                        setTimeout(timeoutFunc, 100)    
                    }
                }
                
            }

            this.$nextTick(function() {
                timeoutFunc()
            })
        },
        onUploadSuccess(response, file, fileList) {
            this.$Spin.hide();
            this.code = ''
            this.fileKey = response.fileKey;
            this.fileTree = [response.fileTree];
            this.syntaxTree = response.syntaxTree
            this.treeResolverValue = travelTree(response.syntaxTree)
            this.treeMap.series[0].data = this.syntaxTree.children
            this.tree.series[0].data = [this.syntaxTree]
        },
        onTreeSelectChange(item) {
            if (item == undefined) {
                return;
            }
            if (item[0].children == undefined) {
                this.browserSpinShow = true;
                const result = this.$axios.get('/api/getFile/' + this.fileKey + '/' + item[0].path)
                .then(response => {
                    this.browserSpinShow = false;
                    this.fileSyntaxTree = response.data.syntaxTree
                    this.fileSyntaxTreeResolverValue = travelTree(response.data.syntaxTree)
                    if (this.fileSyntaxTreeResolverValue.Constructor != undefined) {
                        // concat Constructor to Method
                        this.fileSyntaxTreeResolverValue.Method = this.fileSyntaxTreeResolverValue.Constructor.concat(this.fileSyntaxTreeResolverValue.Method)
                    }
                    this.fullCode = response.data.content
                    this.memberSelected = 'sourceCode';
                    this.onSelectChange(this.memberSelected);
                });
            } else {
                item[0].expand = !item[0].expand
            }
        }
    }
}
</script>
