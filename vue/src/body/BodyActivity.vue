<template>
    <div class="mainLayout" v-if="!ismobile">
        <div class="actHeader" id="actHeader">
            <h1 id="info">历史动态</h1>
        </div>
        <div class="activitiesContent" id="activitiesContent">
            <template v-for="activity in activities">
                <div class="activity">
                    <div class="imgContainer" @click="selectActivity(activity)">
                        <img v-if="activity.img[0]" :src="this.$store.state.url+activity.img[0].img" class="actImg" loading="lazy"/>
                    </div>
                    <div class="actContent" @click="selectActivity(activity)">
                        <span :style="chooseTagStyle()">SDUcraft历史动态</span>
                        <h2 style="margin: 0;padding: 0;">{{ activity.title }}</h2>
                        <span style="font-size: 0.8em; padding: 0;margin: 0;color:#aaaaaa;">{{ activity.summary }}</span>
                        <span style="font-size: 0.85em;">于 <span style="font-weight: bold;">{{ activity.publish_date }}</span> 由 <span style="font-weight: bold;">{{ activity.author }}</span> 发布</span>
                    </div>
                </div>
            </template>
        </div>
    </div>

    <div class="mainLayout" v-else>
        <div class="actHeader" id="actHeader">
            <h1 id="info">历史动态</h1>
        </div>
        <div class="activitiesContent" id="activitiesContent">
            <template v-for="activity in activities">
                <div class="activity">
                    <div class="imgContainer" @click="selectActivity(activity)">
                        <img v-if="activity.img[0]" :src="this.$store.state.url+activity.img[0].img" class="actImg" loading="lazy"/>
                    </div>
                    <div class="actContent" @click="selectActivity(activity)">
                        <!-- <span :style="chooseTagStyle()">SDUcraft历史动态</span> -->
                        <h2 style="margin: 0;padding: 0;">{{ activity.title }}</h2>
                        <span style="font-size: 0.8em; padding: 0;margin: 0;color:#aaaaaa;">{{ activity.summary }}</span>
                        <span style="font-size: 0.85em;">于 <span style="font-weight: bold;">{{ activity.publish_date }}</span> 由 <span style="font-weight: bold;">{{ activity.author }}</span> 发布</span>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default{
    data(){
        return{
            activities:null,
            initHeight:0,
            carousel:null,
            info:null,
        }
    },
    props:['ismobile'],
    watch:{
    },
    mounted(){
        axios.get(this.$store.state.activityAPI).then(response=>{
            this.activities=response.data
        })
        if(this.ismobile){
            this.initHeight=200
        }else{
            this.initHeight=300
        }
        this.carousel = document.getElementById('actHeader');
        this.info = document.getElementById('info');
        window.addEventListener("scroll", this.changeHeaderHeight);
    },
    unmounted(){
        window.removeEventListener("scroll", this.changeHeaderHeight);
    },
    methods:{
        chooseTagStyle(){
            const letters = '0123456789ABCDEF';
            let color = '#';
            for (let i = 0; i < 6; i++) {
                color += letters[Math.floor(Math.random() * 16)];
            }
            return {
                "font-size": "0.2em",
                "color":color
            }
        },
        changeHeaderHeight(){
            const rect=this.carousel.getBoundingClientRect()
            if(rect.top<0 && rect.bottom>0){
                this.info.style.top=Math.min(this.halfInitHeight-0.5*rect.top,this.initHeight-this.info.offsetHeight)+'px'
            }else if(rect.top>0){
                this.info.style.top=this.halfInitHeight+'px'
            }
        },
        selectActivity(selected){
            this.$router.push({name:'activityinline', params:{id:selected.id}})
        }
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
    margin: 0 0%;
    min-height: 100vh;
    font-size: 1.2em;
    background-color: #ffffff;
}
.actHeader{
    height: 300px;
    background-color:antiquewhite;
    position: relative;
}
#info{
    position: absolute;
    top: 50%;
    transform: translate(0, -50%);
    width: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    margin: 0 0;
}
.activitiesContent{
    width: 900px;
    margin: 0 auto;
    padding: 0;
    min-height: calc(100vh - 300px);
}
.activity{
    display: flex;
    width: 100%;
    margin: 30px 0;
}
.imgContainer{
    min-width: 384px;
    min-height: 216px;
    width: 384px;
    height: 216px;
    overflow: hidden;
    cursor: pointer;
}
.actImg{
    width: 384px;
    height: 216px;
    object-fit: cover;
    transform-origin: center center;
    transition: transform 0.3s ease, filter 0.3s ease;
}
.actImg:hover{
    transform: scale(1.1);
    filter: brightness(1.03);
}

.actContent{
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 0 2em;
}
.actContent span,.actContent h2{
    cursor: pointer;
    transition: color 0.2s;
}
.actContent span:hover,.actContent h2:hover{
    color: #999999;
}
@media screen and (max-width: 800px) {
.mainLayout{
    margin: 0 0%;
    min-height: 100vh;
    font-size: 1.2em;
    background-color: #ffffff;
}
.actHeader{
    height: 200px;
}
.activitiesContent{
    width: 100%;
    margin: 0 0;
    padding: 0;
    min-height: calc(100vh - 200px);
}
.activity{
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin: 40px 0;
}
.imgContainer{
    min-width: 90%;
    min-height: 200px;
    width: 90%;
    height: 200px;
    overflow: hidden;
    cursor: pointer;
}
.actImg{
    width: 100%;
    height: 200px;
    object-fit: cover;
    transform-origin: center center;
    transition: transform 0.3s ease, filter 0.3s ease;
}
.actImg:hover{
    transform: scale(1.1);
    filter: brightness(1.03);
}

.actContent{
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    padding: 0 1em;
}
.actContent span,.actContent h2{
    cursor: pointer;
    transition: color 0.2s;
}
.actContent span:hover,.actContent h2:hover{
    color: #999999;
}

}
</style>