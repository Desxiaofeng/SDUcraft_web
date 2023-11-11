<template>
<div class="mainLayout">
    <n-card v-for="proxyServer in proxyServers" :title="proxyServer.name" style="margin-bottom:1em;border: 0px;"  :style="{boxShadow: `var(--el-box-shadow)`}">
        <div style="padding-left: 1em;">
            <span>
            版本：{{ proxyServer.version }}<br>
            地址：{{ proxyServer.host }}<span v-if="proxyServer.port">:{{ proxyServer.port }}</span><br>
            简介：<span v-html="proxyServer.intro"></span>
            </span>
        </div>
        <n-tabs type="line" animated trigger='hover' :default-value="choseDefault(proxyServer.name)">
            <template v-for="server in servers">
            <n-tab-pane :name="server.name" :tab="server.name" v-if="server.proxyServer==proxyServer.id" display-directive="show:lazy">
                <n-carousel v-if="ismobile"
                    effect="fade"
                    style="height: 200px;max-width: 100%;"
                    autoplay
                    draggable
                    trigger="hover"
                    >
                    <template v-for="img in imagesetforserver">
                        <n-carousel-item :style="{ width: '100%' }" v-if="img.server==server.id">
                            <img
                                class="carousel-img"
                                :src="img.img"
                            >
                        </n-carousel-item>
                    </template>
                </n-carousel>
                
                <n-carousel v-else
                    effect="card"
                    prev-slide-style="transform: translateX(-150%) translateZ(-800px);"
                    next-slide-style="transform: translateX(50%) translateZ(-800px);"
                    style="height: 300px;"
                    autoplay
                    draggable
                    trigger="hover"
                    >
                    <template v-for="img in imagesetforserver">
                        <n-carousel-item :style="{ width: '60%' }" v-if="img.server==server.id">
                            <img
                                class="carousel-img"
                                :src="img.img"
                            >
                        </n-carousel-item>
                    </template>
                </n-carousel>

                <span style="padding-left: 1em;display: block;">
                    版本：{{ server.version }}<br>
                    游戏模式：{{ server.mode }}<br>
                    <span v-if="server.host && server.port">直连地址：{{ server.host }}:{{ server.port }}<br></span>
                    跨服指令：/server {{ server.bridge_name }}<br>
                    开服时间：{{ server.init_date }}——{{ server.close_date }}<br>
                    <span v-if="server.author">制作者：{{ server.author }}<br></span>
                    简介：<span v-html="server.intro"></span>
                </span>  
            </n-tab-pane>
            </template>
        </n-tabs>
    </n-card>
            
</div>
</template>


<script>
import axios from 'axios'

export default{
    data(){
        return{
            proxyServers:null,
            servers:null,
            imagesetforserver:null,
        }
    },
    props:['ismobile'],
    mounted(){
        axios.get(this.$store.state.proxyserverAPI).then(response=>{
            this.proxyServers=response.data
        })
        axios.get(this.$store.state.serverAPI).then(response=>{
            this.servers=response.data
        })
        axios.get(this.$store.state.imagesetforserverAPI).then(response=>{
            this.imagesetforserver=response.data
        })
    },
    computed:{

    },
    methods:{
        choseDefault(name){
            if(name=='群组服'){
                return "生存服"
            }else if(name=='校区展示服'){
                return "中心校区"
            }else{
                return "随便吧"
            }
        },
    }
}
</script>

<style scoped>
.carousel-img {
  margin: 0 auto;
  height: 100%;
  object-fit: contain;
}
.mainLayout{
    margin: 0 18% ;
    padding-bottom: 1em;
    min-height: 83vh;
    /* box-shadow: -4px 0 8px rgba(0, 0, 0, 0.2), 4px 0 8px rgba(0, 0, 0, 0.2); */
}
@media screen and (max-width: 800px) {
    .mainLayout{
        margin: 0px;
        background-color: #ffffff;
    }
}

</style>