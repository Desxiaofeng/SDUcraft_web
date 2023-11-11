<template>
    <!-- <div style="background-color: #ffffff;"> -->
        <div class="mainLayout" :style="{boxShadow: `var(--el-box-shadow)`}" >
            <div v-html="md"></div>
        </div>
    <!-- </div> -->
</template>

<script>
import axios from 'axios';
import {marked} from 'marked';

export default{
    data(){
        return{
            showNow:null,
            introductions:null,
            md:null,
        }
    },
    props:['ismobile',"mainImgShow"],
    watch:{
        showNow(){
            axios.get(this.$store.state.url+this.showNow.front_end_address).then(response=>{
                const pathParts = this.showNow.front_end_address.split('/');
                pathParts.pop();
                const url=this.$store.state.url+pathParts.join('/')+'/';
                this.md = marked(response.data).replace(/<img(.*?)src="([^"]*)"/g, '<img$1src="'+url+'$2"');
            }) 
        },
        introductions(){
            if(this.introductions.length>0){
                this.showNow=this.introductions[0]
            }
        },
        md(){
            this.$nextTick(() => {

            });
        },
    },
    mounted(){
        axios.get(this.$store.state.introductionAPI).then(response=>{
            this.introductions=response.data
        })
    },
    methods:{
    }
}
</script>

<style scoped>
.mainLayout{
    margin: 0 18%;
    padding: 2em;
    min-height: 83vh;
    background-color: #ffffff;
    border: 1px solid #cccccc;
    border-bottom: 0;
    border-top: 0;
}
@media screen and (max-width: 800px) {
    .mainLayout{
    margin: 0 0em;
    }
}
</style>