<template>
    <div class="w-container">
        <Row>
            <Upload action="/api/upload" :on-success="onUploadSuccess" :show-upload-list="false">
                <Button type="ghost" icon="ios-cloud-upload-outline">Upload files</Button>
                <span v-if="fileKey != null" style="margin-left: 10px">File Key: {{ fileKey }} </span>
            </Upload>
        </Row>
        <Row>
            <Tabs value="glob" style="height: 100%">
                <TabPane label="Overview" name="glob">
                    <Tabs value="tree" style="height: 100%">
                        <TabPane label="Package and Class Tree" name="tree">
                            <chart :options="tree" style="width: 100%; height: 600px"></chart>
                        </TabPane>
                        <TabPane label="Line of codes" name="treeMap">
                            <chart :options="treeMap" style="width: 100%; height: 600px"></chart>
                        </TabPane>
                    </Tabs>
                    
                </TabPane>
                <TabPane label="Source code browser" name="file">
                    <Row :gutter="20">
                        <iCol :span="6">
                            <Tree :data="fileTree" @on-select-change="onTreeSelectChange"></Tree>
                        </iCol>
                        <iCol :span="18">
                            <Row>
                                <Select v-model="memberSelected" @on-change="onSelectChange">
                                    <Option v-for="(item,index) in fileSourceTree.members" :value="item" :key="index">{{ item }}</Option>
                                </Select>
                            </Row>
                            <Row :gutter="20">
                                <iCol :span="12">
                                    <pre v-highlightjs="code"><code class="x-java"></code></pre>
                                </iCol>
                                <iCol :span="12">
                                    <div style="margin-top: 12px;">
                                        Graph
                                    </div>
                                </iCol>
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

function colorMappingChange(value) {
    var levelOption = getLevelOption(value);
    chart.setOption({
        series: [{
            levels: levelOption
        }]
    });
}

// var formatUtil = echarts.format;

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

export default {
    name: 'app',
    data () {
        return {
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
                        name:'Porject Overview',
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
            memberSelected: '',
            fileSourceTree: {
                members: ['get', 'set']
            },
            code: '',
            fileKey: null,
            fileTree: []
        }
    },
    methods: {
        onSelectChange(value) {
            console.log(value);
        },
        onUploadSuccess(response, file, fileList) {
            this.fileKey = response.fileKey;
            this.fileTree = [response.fileTree];
            this.syntaxTree = response.syntaxTree
            this.treeMap.series[0].data = this.syntaxTree.children
            this.tree.series[0].data = [this.syntaxTree]
            console.log(response, file, fileList);
        },
        onTreeSelectChange(item) {
            if (item[0].children == undefined) {
                console.log(item[0].path)
                const result = this.$axios.get('/api/getFile/' + this.fileKey + '/' + item[0].path)
                .then(response => {
                    console.log(response)
                    this.code = response.data.content
                });
            }
        }
    }
}
</script>
