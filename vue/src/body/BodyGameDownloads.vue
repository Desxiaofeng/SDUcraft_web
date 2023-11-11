<template>
    <div class="mainLayout">
        <div v-for="download in downloads" class="container" :style="{boxShadow: `var(--el-box-shadow)`}">
            <el-image class="container-p1" :src="download.img" fit="cover" />
            <div class="container-p2">
                <div>
                    <h2 style="margin: 0;">{{ download.name }}</h2>
                    <span>
                    发布时间：{{ download.publish_date }}<br>
                    版本：{{ download.version }}<br>
                    作者：{{ download.author }}<br>
                    简介：<span v-html="download.intro"></span>
                    </span>
                </div>
                <n-tabs type="line" animated trigger='hover' default-value="Windows">
                    <template v-for="file in files">
                        <n-tab-pane v-if="file.download==download.id" :tab="file.OS" :name="file.OS" class="download">
                            <a :href="file.file" class="button" v-if="file.file">
                                <div style="text-align: center;font-size: 1.1em;">下  载</div>
                                <div style="text-align: center;font-size: 0.7em;">{{ file.size }}MB</div>
                            </a>
                            <span v-else>高贵的{{ file.OS }}用户要学会自己配置客户端~</span>                 
                            修改时间：{{ file.modify_date }}
                            
                        </n-tab-pane>
                    </template>
                </n-tabs>

            </div>
            
        </div>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    data(){
        return{
            downloads:null,
            files:null,
        }
    },
    mounted(){
        axios.get(this.$store.state.downloadAPI).then(response=>{
            this.downloads=response.data
        }),
        axios.get(this.$store.state.filesetfowdownloadAPI).then(response=>{
            this.files=response.data
        })
    },
}
</script>

<style scoped>
.mainLayout{
    min-height: 83vh;
    display: flex;
    justify-content: center;
    margin: 0 18%;
    flex-wrap: wrap;
}
.container{
    width: 70%;
    display: flex;
    justify-content: center;
    align-items: center;
    border: 1px solid #cccccc;
    margin-bottom: 2em;
    border-radius: 5px;
    padding: 1em;
    background-color: #ffffff;
}
.container-p1{
    width: 200px; 
    height: 200px; 
    margin-right: 2em;
    
}
.container-p2{
    width: 60%;
    
}
.download{
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.button{
    background-color: #67c23a;
    flex: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 0.2em 4em;
    border-radius: 5px;

    text-decoration: none; 
    color: rgb(255, 255, 255); 
    display: block;
}
.button:hover{
    background-color: #95d475;
}

@media screen and (max-width: 800px) {
    .container{
        flex-direction: column;
        width: 100%;
        padding: 2em;
    } 
    .container-p1{
        margin-right: 0;
    }
    .container-p2{
        width: 100%;
    }
    .mainLayout{
        margin: 0px;
        background-color: #ffffff;
    }
}

</style>