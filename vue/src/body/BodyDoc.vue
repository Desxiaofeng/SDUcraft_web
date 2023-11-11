<template>
    <div class="mainLayout" :style="{boxShadow: `var(--el-box-shadow)`}">
        <n-breadcrumb>
            <n-breadcrumb-item>更多</n-breadcrumb-item>
            <n-breadcrumb-item @click="changeurl()">文档&教程</n-breadcrumb-item>
            <n-breadcrumb-item v-if="md">{{ docNow.title }}</n-breadcrumb-item>
        </n-breadcrumb>
        <template v-for="doc in documents" v-if="!md">
            <div v-if="doc.front_end_address.endsWith('.md')" class="content">
                <span>{{ doc.publish_date }}：<a href="#" @click.prevent="changeurl(doc.id)">{{ doc.title }}</a></span>
            </div>
            <div v-else class="content">
                <span>{{ doc.publish_date }}：<a :href="this.$store.state.url+doc.front_end_address">{{ doc.title }}</a></span>
            </div>
        </template>
        <div v-else v-html="md"></div>

</div>
</template>

<script>
import axios from 'axios';
import {marked} from 'marked';

export default{
    data(){
        return{
            documents:null,
            docNow:null,
            md:null,
        }
    },
    props:['ismobile'],
    watch:{
        documents(){
            this.$router.replace({path:this.$route.fullPath, query:{id:this.$route.query.id,random:Math.random()}})
        },
    },
    mounted(){
        axios.get(this.$store.state.documentAPI).then(response=>{
            this.documents=response.data
        })
    },
    methods:{
        showMD(doc){
            axios.get(this.$store.state.url+doc.front_end_address).then(response=>{
                this.docNow=doc
                const pathParts = doc.front_end_address.split('/');
                pathParts.pop();
                const url=this.$store.state.url+pathParts.join('/')+'/';
                this.md = marked(response.data).replace(/<img(.*?)src="([^"]*)"/g, '<img$1src="'+url+'$2"');
            }) 
        },
        chooseMD(id){
            this.documents.forEach(doc=>{
                if(doc.id==id){
                    this.showMD(doc)
                    return
                }else{
                    this.md=null
                }
            })
        },
        changeurl(selectedId=null){
            if(selectedId){
                this.$router.push({path:this.$route.fullPath,query:{id:selectedId,random:Math.random()}})
            }else{
                this.$router.push({path:this.$route.fullPath,query:{random:Math.random()}})
            }
            
        }
    },
    beforeRouteUpdate(to, from){
        if(!to.query['id']){
            this.md=null
        }else{
            this.chooseMD(to.query['id'])
        }
    }
}
</script>

<style scoped>
.mainLayout{
    margin: 0 18%;
    min-height: 90vh;
    border: 1px solid #cccccc;
    padding: 1em 10%;
    font-size: 1.2em;
    background-color: #ffffff;
}
.content{
    
    display: flex;
    align-items: center;
    justify-content:flex-start;
    padding: 0.5em 0;
}
@media screen and (max-width: 800px) {
    .mainLayout{
        margin: 0em;
        padding: 2em;
        font-size: 1em;
    }
    .content{
    padding: 0 em;
    }
}
</style>