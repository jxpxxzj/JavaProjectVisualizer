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
                <TabPane label="概览" name="glob">
                    标签一的内容
                </TabPane>
                <TabPane label="浏览" name="file">
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
export default {
    name: 'app',
    data () {
        return {
            memberSelected: '',
            fileSourceTree: {
                members: ['get', 'set']
            },
            code: '',
            fileKey: '',
            fileTree: []
        }
    },
    methods: {
        onSelectChange(value) {
            console.log(value);
        },
        onUploadSuccess(response, file, fileList) {
            this.fileKey = response.fileKey;
            this.fileTree = [response.tree];
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
