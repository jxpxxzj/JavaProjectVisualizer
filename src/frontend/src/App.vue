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
                                    <TabPane :label="`Package (${treeResolverValue.Package.length})`" name="package">
                                        <Table border height="550" :columns="tableCols.package" :data="treeResolverValue.Package"></Table>
                                    </TabPane>
                                    <TabPane :label="`Class (${treeResolverValue.Class.length})`" name="class">
                                        <Table border height="550" :columns="tableCols.class" :data="treeResolverValue.Class"></Table>
                                    </TabPane>
                                    <TabPane :label="`Constructor (${treeResolverValue.Constructor.length})`" name="constructor">
                                        <Table border height="550" :columns="tableCols.constructor" :data="treeResolverValue.Constructor"></Table>
                                    </TabPane>
                                    <TabPane :label="`Method (${treeResolverValue.Method.length})`" name="method">
                                        <Table border height="550" :columns="tableCols.method" :data="treeResolverValue.Method"></Table>
                                    </TabPane>
                                    <TabPane :label="`Field (${treeResolverValue.Field.length})`" name="field">
                                        <Table border height="550" :columns="tableCols.field" :data="treeResolverValue.Field"></Table>
                                    </TabPane>
                                    <TabPane :label="`Interface (${treeResolverValue.Interface.length})`" name="interface">
                                        <Table border height="550" :columns="tableCols.interface" :data="treeResolverValue.Interface"></Table>
                                    </TabPane>
                                    <TabPane :label="`Interface Method (${treeResolverValue.InterfaceMethod.length})`" name="interfaceMethod">
                                        <Table border height="550" :columns="tableCols.interfaceMethod" :data="treeResolverValue.InterfaceMethod"></Table>
                                    </TabPane>
                                    <TabPane :label="`Annotation (${treeResolverValue.Annotation.length})`" name="annotation">
                                        <Table border height="550" :columns="tableCols.annotation" :data="treeResolverValue.Annotation"></Table>
                                    </TabPane>
                                    <TabPane :label="`Annotation Method (${treeResolverValue.AnnotationTypeElement.length})`" name="annotationTypeElement">
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
                        <iCol :span="18">
                            <Row>
                                <Select v-model="memberSelected" @on-change="onSelectChange">
                                    <Option value="sourceCode">Source Code</Option>
                                    <Option v-for="(item,index) in fileSourceTree.members" :value="item" :key="index">{{ item }}</Option>
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
                                                <TabPane label="Control Flow Graph">
                                                    Graph
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
import { travelTree } from './syntaxTreeResolver'

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
                        zoomToNodeRatio: 0.36,
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
            memberSelected: 'sourceCode',
            fileSourceTree: {
                members: ['get', 'set']
            },
            code: '',
            fileKey: null,
            fileTree: []
        }
    },
    methods: {
        onBeforeUpload() {
            this.$Spin.show();
            return true;
        },
        onMenuChange(name) {
            this.activeMenu = name
        },
        onSelectChange(value) {
            hljs.initLineNumbersOnLoad();
        },
        onUploadSuccess(response, file, fileList) {
            this.$Spin.hide();
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
                    console.log(response)
                    this.code = response.data.content
                });
            } else {
                item[0].expand = !item[0].expand
            }
        }
    }
}
</script>
