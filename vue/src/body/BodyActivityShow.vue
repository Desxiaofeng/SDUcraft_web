<template>
    <div class="mainLayout" v-if="!ismobile">
        <div class="carousel" v-if="activity" id="carousel">
            <div class="info" id="info">
                <h1 style="margin-bottom: 0.4em;">{{ activity.title }}</h1>
                <div style="font-size: 0.85em;display: flex;flex-direction: column;justify-content: center;">
                    <span style="display: flex;justify-content: center;">于 <span style="font-weight: bold;">{{ activity.publish_date }}</span> 由 <span style="font-weight: bold;">{{ activity.author }}</span> 发布</span>
                    <span style="display: flex;justify-content: center;align-items: center;"><el-icon><i-ep-Histogram /></el-icon>字数：{{ activity.wordCount/1000 }}&emsp;&emsp;<el-icon><i-ep-Reading /></el-icon>阅读：{{ activity.clicks }}</span>
                </div>
                
            </div>
            <el-carousel :height="initHeight+'px'" :interval=10000>
                <el-carousel-item v-for="img in activity.img" 
                :style="{
                'background-image': 'url('+this.$store.state.url+img.img+')',
                'background-repeat': 'no-repeat',
                'background-size': 'cover',
                'background-position':'center center',}"
                >
                <div style="background-color: rgba(0, 0, 0, 0.3);z-index: 2;width: 100%;height: 100%;"></div>
                </el-carousel-item>
            </el-carousel>
        </div>

        <div class="content">
            <n-breadcrumb>
            <n-breadcrumb-item>社区</n-breadcrumb-item>
            <n-breadcrumb-item @click="backList()">历史动态</n-breadcrumb-item>
            <n-breadcrumb-item v-if="activity">{{ activity.title }}</n-breadcrumb-item>
            </n-breadcrumb>
            <div v-html="html"></div>
        </div>
    </div>

    <div class="mainLayout" v-else>
        <div class="carousel" v-if="activity" id="carousel">
            <div class="info" id="info">
                <h1 style="margin-bottom: 0.4em;">{{ activity.title }}</h1>
                <div style="font-size: 0.85em;display: flex;flex-direction: column;justify-content: center;">
                    <span style="display: flex;justify-content: center;">于 <span style="font-weight: bold;">{{ activity.publish_date }}</span> 由 <span style="font-weight: bold;">{{ activity.author }}</span> 发布</span>
                    <span style="display: flex;justify-content: center;align-items: center;"><el-icon><i-ep-Histogram /></el-icon>字数：{{ activity.wordCount/1000 }}&emsp;&emsp;<el-icon><i-ep-Reading /></el-icon>阅读：{{ activity.clicks }}</span>
                </div>
                
            </div>
            <el-carousel :height="initHeight+'px'" :interval=10000>
                <el-carousel-item v-for="img in activity.img" 
                :style="{
                'background-image': 'url('+this.$store.state.url+img.img+')',
                'background-repeat': 'no-repeat',
                'background-size': 'cover',
                'background-position':'center center',}"
                >
                <div style="background-color: rgba(0, 0, 0, 0.3);z-index: 2;width: 100%;height: 100%;"></div>
                </el-carousel-item>
            </el-carousel>
        </div>

        <div class="content">
            <n-breadcrumb>
            <n-breadcrumb-item>社区</n-breadcrumb-item>
            <n-breadcrumb-item @click="backList()">历史动态</n-breadcrumb-item>
            <n-breadcrumb-item v-if="activity">{{ activity.title }}</n-breadcrumb-item>
            </n-breadcrumb>
            <div v-html="html"></div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            activity:null,
            html:null,
            initHeight:null,
            carousel:null,
            info:null,
        }
    },
    props:['ismobile'],
    watch:{
        activity(){
            axios.get(this.$store.state.url+this.activity.front_end_address).then(response=>{
                const pathParts = this.activity.front_end_address.split('/');
                pathParts.pop();
                const url=this.$store.state.url+pathParts.join('/')+'/';
                this.html = response.data.replace(/<img(.*?)src="([^"]*)"/g, '<img$1src="'+url+'$2"');
            }) 
        },
        html(){
            this.carousel = document.getElementById('carousel');
            this.info = document.getElementById('info');
            window.addEventListener("scroll", this.changeHeaderHeight);
        }
    },
    mounted(){
        axios.get(this.$store.state.activityAPI+this.$route.params.id).then(response=>{
            this.activity=response.data
        })
        if(this.ismobile){
            this.initHeight=250
        }else{
            this.initHeight=400
        }
    },
    unmounted(){
        window.removeEventListener("scroll", this.changeHeaderHeight);
    },
    methods:{
        backList(){
            this.$router.push({name:'activity'})
        },
        changeHeaderHeight(){
            if(this.ismobile){
                return
            }
            const rect=this.carousel.getBoundingClientRect()
            if(rect.top<0 && rect.bottom>0){
                this.info.style.top=Math.min(this.halfInitHeight-0.5*rect.top,this.initHeight-this.info.offsetHeight)+'px'
            }else if(rect.top>0){
                this.info.style.top=this.halfInitHeight+'px'
            }
        },
    },
    computed:{
        halfInitHeight(){
            return 0.5*this.initHeight
        },
    }
}
</script>

<style scoped>
.mainLayout{
    margin: 0 0;
    min-height: 100vh;
    font-size: 1.1em;
    background-color: #ffffff;
}
.carousel{
    position: relative;
    font-size: 1.1em;
}
.info{
    position: absolute;
    top: 50%;
    transform: translate(0, -50%);
    z-index: 1;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #ffffff;
}
.content{
    margin: 0 25%;
    padding: 0.5em 0;
}
@media screen and (max-width: 800px) {
.mainLayout{
    margin: 0 0;
    min-height: 100vh;
    font-size: 1em;
    background-color: #ffffff;
}
.carousel{
    position: relative;
    font-size: 1.1em;
}
.info{
    position: absolute;
    top: 50%;
    transform: translate(0, -50%);
    z-index: 1;
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #ffffff;
    margin: 0;
    padding: 0;
}
.content{
    margin: 0 0;
    padding: 0.5em 1em;
}
*{
    /* overflow-x: auto; */
    overflow-y: hidden;
    word-wrap: break-word;
    overflow-wrap: break-word;
    text-wrap: wrap;
}
}
</style>