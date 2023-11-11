<template>
    <n-config-provider preflight-style-disabled>
    <div class="mianCSS" style="overflow: visible;">
        <Header v-if="isIndex"></Header>
        <navm :isNotice="isNotice" :ismobile="ismobile" @changeNoticeBar="handleChangeNoticeBar"></navm>
        <div v-if="!ismobile" :style="mainImgShow" class="forBGIMG" id="beforeBlur">
            <div id="blur" :style="{'--blur': blurValue+'px'}">
                <router-view 
                :state="state" 
                :ismobile="ismobile" 
                >
                </router-view>
            </div>
        </div>
        <div v-else>
            <router-view 
                :state="state" 
                :ismobile="ismobile" 
                :mainImgShow="mainImgShow"
            >
            </router-view>
        </div>
        <Footer></Footer>
    </div>
    </n-config-provider>
</template>

<script>
import Header from "./components/Header.vue"
import Footer from "./components/Footer.vue"
import navm from "./components/nav.vue"
import axios from 'axios'
export default {
    data() {
        return {
            state:false,
            ismobile:false,
            imagesetforproxyserver:[],
            imageNow:null,
            mainImgShow:null,
        }
    },
    components: {
        Header,
        Footer,
        navm,
    },
    methods:{
        handleChangeNoticeBar(){
            this.state=!this.state
        },
        checkMobileDevice() {
            this.ismobile = window.innerWidth < 800;
        },
        loopForImg(len){
            const r=Math.floor(Math.random()*len)
            this.imageNow=this.imagesetforproxyserver[r].img
            this.mainImgShow={
                'background-image': `url(${this.imageNow})`,
                'background-position': 'center center',
                'transition': `background-image 1s`,
                'background-repeat': 'no-repeat',
                'background-size': 'cover',
            }
            setTimeout(()=>{
                this.loopForImg(len)
            },30000)
        },
    },
    computed:{
        blurValue(){
            if(this.isIndex){
                return 0
            }else{
                return 3
            }
        },
        isIndex(){
            return this.$route.name=='index'
        },
        isNotice(){
            return this.$route.name=='notice'
        }
    },
    mounted(){
        this.checkMobileDevice()
        window.addEventListener("resize", this.checkMobileDevice);
        axios.get(this.$store.state.imagesetforproxyserverAPI).then(response=>{
            this.imagesetforproxyserver=response.data
            const len=this.imagesetforproxyserver.length
            if(len>0){
                this.loopForImg(len)
            }
        })
        
    },
    unmounted(){
        window.removeEventListener("resize", this.checkMobileDevice);
    },

}
</script>
<style>
.mainCSS{
    display: flex; 
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    margin: 0;
    padding: 0;
    min-height: 83vh;
}
table {
  border-collapse: collapse;
  border: 1px solid black;
}
th, td {
    border: 1px solid black;
    padding: 8px;
}
code {
    background-color: #f2f2f2;
    padding: 0px 4px;
    border: 0px solid #d1d1d1;
    border-radius: 3px;
}
pre{
    text-wrap: wrap;
}
@media screen and (max-width: 800px) {


}
body {
  font-family:"Microsoft YaHei",Arial,Helvetica,sans-serif,"宋体";
  line-height: 1.5;
}

img {
  max-width: 100%; /* 设置最大宽度为容器的最大宽度 */
  height: auto; /* 设置高度为自动，以保持宽高比 */
}
.forBGIMG{
    background-attachment: fixed;
}
#beforeBlur{
    z-index: -1;
}
#blur:before{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    content: '';
    backdrop-filter: blur(var(--blur));
    z-index: -1;
}
#blur{
    position: relative;
    z-index: 1;
}
</style>
