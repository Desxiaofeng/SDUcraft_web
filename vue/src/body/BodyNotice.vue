<!-- 这个页面的逻辑似乎有点乱，开摆！ -->
<template>
<div class="mainLayout" @touchstart="handleTouchStart" @touchend="handleTouchEnd(100)">
    
    <aside v-if="!ismobile" class="sidebar custom-scrollbar" :style="{boxShadow: `var(--el-box-shadow)`}">
    <div class="sidebar-header nowarp" :style="{boxShadow: `var(--el-box-shadow-lighter)`}">
        <el-icon size="1.8em" color="#222222"><i-ep-Tickets /></el-icon>
        <p style="font-size: 1.1em; margin: auto 0;">公告列表：</p>
    </div>
    <div v-for="notice in notices" :class="{'sidebar-content':true, 'sidebar-content-selected':isSelected(notice)}" :style="chooseType(notice.valid)">
        <a href="#" @click.prevent="changeurl(notice.id)">
            <div class="nowarp">
                <span>
                    {{ notice.publish_date }}
                </span>
                <span v-if="notice.valid==0" style="text-decoration: line-through;">
                    {{ notice.title }}
                </span>
                <span v-else>
                    {{ notice.title }}
                </span>
                <div v-if="notice.valid==2" class="notice-tag notice-tag2">
                    <span>置顶</span>
                </div>
                <div v-if="notice.valid==3" class="notice-tag notice-tag3">
                    <span>重要</span>
                </div>
            </div>
        </a>
    </div>
    </aside>

    <nut-popup v-else position="left" v-model:visible="isShowList" style="width: 62%; height: 100%">

    <aside class="sidebar custom-scrollbar" :style="{boxShadow: `var(--el-box-shadow)`}">
        <div class="sidebar-header nowarp" :style="{boxShadow: `var(--el-box-shadow-lighter)`}">
            <el-icon size="1.8em" color="#222222"><i-ep-Tickets /></el-icon>
            <p style="font-size: 1.1em; margin: auto 0;">公告列表：</p>
            <el-icon size="1.8em" color="#222222" @click="changeNoticesList" @touchstart="handleTouchStart" @touchend="handleTouchEnd(25)"><i-ep-DArrowLeft/></el-icon>
        </div>
        <div v-for="notice in notices" :class="{'sidebar-content':true, 'sidebar-content-selected':isSelected(notice)}" :style="chooseType(notice.valid)">
            <a href="#" @click.prevent="changeurl(notice.id)">
                <div class="nowarp">
                    <span>
                        {{ notice.publish_date }}
                    </span>
                    <span v-if="notice.valid==0" style="text-decoration: line-through;">
                        {{ notice.title }}
                    </span>
                    <span v-else>
                        {{ notice.title }}
                    </span>
                    <div v-if="notice.valid==2" class="notice-tag notice-tag2">
                        <span>置顶</span>
                    </div>
                    <div v-if="notice.valid==3" class="notice-tag notice-tag3">
                        <span>重要</span>
                    </div>
                </div>
            </a>
        </div>
    </aside>

    </nut-popup>

    <div class="content-content" ref="mdcontent" @click="makeHide">
        <div v-html="md" class="flowhandle"></div>
    </div>

    <aside class="sidebar-right custom-scrollbar">
        <div v-for="header in headers" :class="{'sidebar-content-right':true,'sidebar-content-selected-right':this.currentHeader==header}">
            <a href="#" @click.prevent="scrollToHeader(header)">
                <div class="nowarp">
                    <span :class="anchorClass(header)">
                        {{ header.outerText }}
                    </span>
                </div>
            </a>
        </div>
    </aside>
</div>
</template>

<script>
import axios from 'axios';
import {marked} from 'marked';


export default{
    data(){
        return{
            notices:null,
            showNow:null,
            md:null,
            headers:[],
            currentHeader:null,
            touchStartX:0,
            touchEndX:0,
            timeNow:0,
            isShowList:false,
        }
    },
    props:["state",'ismobile'],
    components:{
    },
    methods:{
        changeNotice(id, isTransHeader){
            let isfind=0
            this.notices.forEach(notice =>{
                if(notice.id==id){
                    this.showNow=notice
                    isfind=1
                }
            })
            if(isfind==0){
                if(this.notices.length>0){
                    for (let i = 0; i < this.notices.length; i++) {
                        let notice = this.notices[i];
                        if (notice.valid !== 0) {
                            this.showNow = notice;
                            break; // 跳出整个循环
                        }
                    }
                    isTransHeader=false
                }
            }
            if(isTransHeader){
                this.$router.replace({path:this.$route.fullPath, query:{id:this.showNow.id,header:this.$route.query.header}})
            }else{
                this.$router.replace({path:this.$route.fullPath, query:{id:this.showNow.id}})
            }
            
        },
        changeurl(selectedId){
            this.$router.push({path:this.$route.fullPath, query:{id:selectedId}})
        },
        changeNoticeForRouteUpdate(id){
            let isfind=0
            this.notices.forEach(notice =>{
                if(notice.id==id){
                    this.showNow=notice
                    isfind=1
                }
            })
            if(isfind==0){
                if(this.notices.length>0){
                    this.showNow=this.notices[0]
                }
            }
        },
        isSelected(notice){
            if(notice.id==this.showNow.id){
                return true
            }
            return false
        },
        generateHeaders(header) {
            this.headers = Array.from(this.$refs.mdcontent.querySelectorAll("h1,h2,h3,h4"));
            for (const heading of this.headers) {
                if (header==heading.outerText) {
                    this.scrollToHeader(heading)
                    return;
                }
            }
            window.scrollTo({
                top: 0,
                behavior: 'smooth' // 可以添加平滑滚动效果
            });
        },
        scrollToHeader(header){
            header.scrollIntoView({behavior: "smooth", block: "start" })
        },
        updateCurrentTitle() {
            for (const heading of this.headers) {
                const rect = heading.getBoundingClientRect();
                if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
                    this.currentHeader = heading;
                    this.$router.replace({path:this.$route.fullPath, query:{id:this.showNow.id,header:this.currentHeader.outerText}})
                    return;
                }
            }
            this.currentHeader = "";
        },
        anchorClass(header){
            return {
                'anchorH1':header.localName=='h1',
                'anchorH2':header.localName=='h2',
                'anchorH3':header.localName=='h3',
                'anchorH4':header.localName=='h4',
            }
        },
        changeNoticesList(){
            this.isShowList=!this.isShowList
        },
        makeHide(){
            if(this.ismobile==true){
                this.isShowList=false
            }
        },
        handleTouchStart(){
            this.touchStartX=event.touches[0].clientX;
            this.timeNow=Date.now()
        },
        handleTouchEnd(move) {
            this.touchEndX = event.changedTouches[0].clientX;
            this.handleSwipe(move,Date.now()-this.timeNow);
        },
        handleSwipe(move,time) {
        const swipeDistance =  this.touchEndX-this.touchStartX;
            if(time>300){
                return
            }
            if (swipeDistance > move) { 
                this.isShowList = true;
            } else if(swipeDistance<-move){
                this.isShowList = false;
            }
        },
        chooseType(valid){
            if(valid==0){
                return {
                    'border-left': '4px solid #888888'
                }
            }else if(valid==1){
                return {
                    'border-left': '4px solid #50d4ab'
                }
            }else if(valid==2){
                return {
                    'border-left': '4px solid #1677ff'
                }
            }else if(valid==3){
                return {
                    'border-left': '4px solid #f66f6a'
                }
            }
        }
    },
    mounted(){
        axios.get(this.$store.state.noticeAPI).then(response=>{
            this.notices=response.data
        })
        window.addEventListener("load", this.updateCurrentTitle);
        window.addEventListener("scroll", this.updateCurrentTitle);
    },
    unmounted(){
        window.removeEventListener("load", this.updateCurrentTitle);
        window.removeEventListener("scroll", this.updateCurrentTitle);
    },
    watch:{
        showNow(){
            axios.get(this.$store.state.url+this.showNow.front_end_address).then(response=>{
                const pathParts = this.showNow.front_end_address.split('/');
                pathParts.pop();
                const url=this.$store.state.url+pathParts.join('/')+'/';
                this.md = marked(response.data).replace(/<img(.*?)src="([^"]*)"/g, '<img$1src="'+url+'$2"');
            }) 
        },
        notices(){
            //没有valid=3则按时间排序，有valid=3先显示valid=3，除非指定了id
            this.changeNotice(this.$route.query.id,true)
            this.notices.sort((a, b) => {
                const validOrder = [3, 2, 1, 0];
                const validA = validOrder.indexOf(a.valid);
                const validB = validOrder.indexOf(b.valid);
                return validA - validB;
            });
            //重新选择valid=3作为首个展示的notice
            if(this.notices.length>0){
                if(this.notices[0].valid==3){
                    this.changeNotice(this.$route.query.id,true)
                }
            }
        },
        md(){
            this.$nextTick(() => {
                this.generateHeaders(this.$route.query.header);
            });
        },
        state(){
            this.changeNoticesList()
        }
    },
    beforeRouteUpdate(to, from){
        if(to.query['id']!=from.query['id']){
            this.changeNoticeForRouteUpdate(to.query['id'])
        }
    }
}
</script>

<style scoped>

.mainLayout{
    display: flex;
    flex-direction: row;
    overflow: visible;
    min-height: 83vh;
    background-color: #ffffff;
}
.sidebar{
    text-align: center;
    display: flex;
    flex-direction: column;
    height: 100vh;
    flex: 0 0 18%;
    position:sticky;
    top:0;
    overflow-y: auto;
    border-right: 1px solid #d0d7de;

}
.sidebar-header{
    display: flex;
    align-items: center;
    padding-left: 0.5em;
    position:sticky;
    top:0;
    min-height: 4em;
    background-color:#ffffff;
    z-index: 2;
}
.sidebar-content{
    margin: 0.5em 0.5em 0em 0.5em;
    border-radius: 3px;
    min-height: 4em;
    font-size: 0.85em;
}
.sidebar-content div{
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding-left: 1em;
    align-items: flex-start;
}
a{
    text-decoration: none;
    color: #000;
}

.sidebar-content:hover{
    background-color: #f3f3f5;
}
.sidebar-content-selected{
    background-color: #e7f5ee;
    color: #18a058;
}
.sidebar-content-selected a{
    color: #18a058;
}
.nowarp{
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden ;
}
.nowarp *{
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden ;
}
.notice-tag{
    background-color: #ebffd7;
    color: #58c622;
    position: absolute;
    margin-bottom: 2em;
    right: 1em;
    width: 3.5em;
    max-height: 1.7em;
    border-radius: 4px;
    text-align: center;
    flex-direction: row;
    align-items: center !important;
    padding-left: 0 !important;
    font-size: 0.8em;
}
.notice-tag0{
    background-color: #eeeeee;
    color: #777777;
}
.notice-tag1{
    background-color: #ebffd7;
    color: #58c622;
}
.notice-tag2{
    background-color: #d1eafd;
    color: #1677ff;
}
.notice-tag3{
    background-color: #fde0d1;
    color: #ff0000;
}
.content-content{
    margin: 1em;
    margin-top: 0;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}
.content-content div{
    margin: 1em;
    padding: 0;
}

.sidebar-right{
    display: flex;
    flex-direction: column;
    flex: 0 0 15%;
    align-self: start;
    max-height: 100vh;
    position:sticky;
    top:10vh;
    overflow-y: auto;
}
.sidebar-content-right{
    margin: 0 1em 0 0;
    border-left: 2px solid #d0d7de;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    min-height: 1.8em;
    font-size: 0.8em;
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.sidebar-content-right div{
    height: 100%;
    display: flex;
    align-items: center;
}
.sidebar-content-right:hover{
    background-color: #f3f3f5;
}
.sidebar-content-selected-right{
    background-color: #e7f5ee;
    border-left: 3px solid #18a058;
    transition: border-left 0.1s;
    position:sticky;
    bottom: 0;
}
.sidebar-content-selected-right a{
    color: #18a058;
}
.anchorH1{
    padding-left: 1em;
}
.anchorH2{
    padding-left: 2em;
}
.anchorH3{
    padding-left: 3em;
}
.anchorH4{
    padding-left: 4em;
}
.buttonRight{
    background-color: #ffffff;
    cursor: pointer;
    display: inline-block;
    border-radius: 50%;
    margin: 0;
    padding: 0;
}

@media screen and (max-width: 800px) {
    .sidebar-right{
        display: none;
    }
    .sidebar-header{
        justify-content: space-between;
    }
    .content-header{
    margin: 5px 5px 0px;
    }
    .content-content{
    margin: 5px;
    }

    *{
    /* overflow-x: auto; */
    overflow-y: hidden;
    word-wrap: break-word;
    overflow-wrap: break-word;
    text-wrap: wrap;
    }

}
.hideSidebar{
    display: none;
}


/* 自定义滚动条轨道 */
.custom-scrollbar::-webkit-scrollbar {
    width: 4px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: #f1f1f1;
}

/* 自定义滚动条滑块 */
.custom-scrollbar::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
}

/* 鼠标悬停时的滑块样式 */
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: #555;
}


</style>