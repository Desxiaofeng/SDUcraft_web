<template>
<!-- 名字 版本 大小 发布时间 修改时间 地址 -->
    <div class="mainLayout" :style="{boxShadow: `var(--el-box-shadow)`}">
        <div class="itemLayout" style="border-bottom: 2px solid #cccccc;">
            <div>name</div>
            <div>type</div>
            <div>time</div>
            <div>size</div>
        </div>
        <div class="itemLayout">
            <div>
            <a href="#" @click.prevent="getOut()">
                ..
            </a>
            </div>
            <div></div>
            <div></div>
            <div></div>
        </div>
        <div class="itemLayout" v-for="download in downloads">
            <div>
            <a href="#" @click.prevent="DownloadOrGetIn(download)">
                {{ download.name }}
            </a>
            </div>
            <div>{{ download.type }}</div>
            <div>{{ download.mtime }}</div>
            <div v-if="download.size">{{ (download.size/1024/1024).toFixed(3) }} MB</div>
            <div v-else></div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    data(){
        return{
            downloads:null,
            urlNow:null,
        }
    },
    mounted(){
        this.urlNow=this.$store.state.otherdownloadAPI
        this.getIn()
    },
    methods:{
        DownloadOrGetIn(download){
            if(download.type=='directory'){
                this.urlNow=this.urlNow+'/'+download.name
                this.getIn()
            }else{
                window.open(this.urlNow+'/'+download.name)
            }
        },
        getIn(){
            axios.get(this.urlNow+'/').then(response=>{
                this.downloads=response.data
            })
        },
        getOut(){
            if(this.urlNow!=this.$store.state.otherdownloadAPI){
                this.urlNow=this.urlNow.substring(0, this.urlNow.lastIndexOf('/'))
            }
            this.getIn()
        }
    }
}
</script>

<style scoped>
.mainLayout{
    display: flex;
    flex-direction: column;
    margin: 0 18%;
    min-height: 83vh;
}
.itemLayout:nth-child(odd){
    display: flex;
    justify-content: space-around;
    background-color: rgb(255, 255, 255);
    font-size: large;
    width: 100%;
}
.itemLayout:nth-child(even){
    display: flex;
    justify-content: space-around;
    background-color: rgb(255, 255, 255);
    font-size: large;
    width: 100%;
}
.itemLayout div:nth-child(1){
    width: 30%;
}
.itemLayout div:nth-child(2){
    width: 20%;
}
.itemLayout div:nth-child(3){
    width: 30%;
}
.itemLayout div:nth-child(4){
    width: 10%;
}
.itemLayout{
    padding: 0.2em 0;
}
a{
    text-decoration: none;
    color:cornflowerblue
}
@media screen and (max-width: 800px) {
    .mainLayout{
        margin: 0px;
    }
    *{
    overflow-x: auto;
    overflow-y: visible;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
}
</style>