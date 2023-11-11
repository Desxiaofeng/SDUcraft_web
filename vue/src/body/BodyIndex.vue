<template>
    <div class="main" v-if="!ismobile">
        <div class="aboutUs" id="Height">
            <h1 style="text-align: center;margin: 1em 0 0.2em 0;">Welcome to the SDUcraft!</h1>
            <p style="padding: 0 1.5em;margin: 0.5em;">
                这里是一校三地八校区山大人共同的MC家园，欢迎您的加入！
                在这里您可以自由地与其他山大MC人交流关于包括但不限于生存、红石、建筑和模组等方面的内容。
                同时，这里还维护有众多MC服务器，期待您与其他山大MC人一同探索。
            </p>
            <div style="margin: 1em 1em 1em 1em;text-align: center;">目前我们的聚集地在QQ群:<br>981809412</div>
            <div style="display: flex; justify-content: space-between;width: 100%;">
                <button @click="changePage('intro')">关于我们&ensp;<el-icon size="1.5em"><i-ep-Right /></el-icon></button>
            </div>
        </div>
    </div>
    <div class="mianForMobile" v-if="ismobile">
        <div :style="mainImgShow" style="width: 100%; height: 250px;">
        </div>
        <div class="aboutUsForMobile">
            <h1 style="text-align: center;margin: 0.5em 0 0.2em 0;">Welcome to the SDUcraft!</h1>
            <p style="padding: 0 1em;margin: 0.2em;">
                这里是一校三地八校区山大人共同的MC家园，欢迎您的加入！
                在这里您可以自由地与其他山大MC人交流关于包括但不限于生存、红石、建筑和模组等方面的内容。
                同时，这里还维护有众多MC服务器，期待您与其他山大MC人一同探索。
            </p>
            <div style="display: flex; justify-content: space-between;width: 100%;">
            <button @click="changePage('intro')">关于我们&ensp;<el-icon size="1.5em"><i-ep-Right /></el-icon></button>
            <span style="margin: 1em 3em 1em 1em;">目前我们的聚集地在<br>QQ群：981809412</span>
            </div>
        </div>
    </div>
    <div class="part">
        <div class="partsmall" @click="changePage('notice')">
            <p style="text-align: center;margin: 30% 15% 0 15%; color: #ffffff;padding-bottom: 20px; border-bottom: 4px solid #ffffff;">
                确定不来看看我们最近在干嘛吗？
            </p>
            <p style="text-align: center;margin: 4% 15% 0 15%; color: #ffffff;">
                哼，爱看不看!
            </p>
            </div>
        <div :style="chooseImg(imagesetforserver)" class="partbig" @click="changePage('serverList')" >
            <div class="subbig"> 
            <p style="text-align: center;margin: 30% 15% 0 15%; color: #ffffff;padding-bottom: 20px; border-bottom: 4px solid #ffffff;">
                学累了？快来一起玩!
            </p>
            <p style="text-align: center;margin: 3% 15% 0 15%; color: #ffffff;">
                我们运营了这这这这这这么多的MC服务器!
            </p>
            </div> 
        </div>
    </div>
    <div class="part">
        <div class="partbig1" @click="jumpLink()">
            <div class="subbig1">
            <p style="text-align: center;margin: 23% 15% 0 15%; color: #ffffff;padding-bottom: 20px; border-bottom: 4px solid #ffffff;">
                没空上线？来云游我们的生存服！
            </p>
            <p style="text-align: center;margin: 3% 15% 0 15%; color: #ffffff; text-decoration: line-through;">
                我才不会告诉你它又卡又耗带宽
            </p>
            </div>
        </div>
        <div class="partsmall1" @click="changePage('game')">
            <p style="text-align: center;margin: 43% 15% 0 15%; color: #ffffff;padding-bottom: 20px; border-bottom: 4px solid #ffffff;">
                没有客户端？
            </p>
            <p style="text-align: center;margin: 4% 15% 0 15%; color: #ffffff;">
                来下载我们准备的整合包!
            </p>
        </div>
    </div>

</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
            imagesetforserver:[],
        }
    },
    props:['ismobile','mainImgShow'],
    mounted(){
        axios.get(this.$store.state.imagesetforserverAPI).then(response=>{
            this.imagesetforserver=response.data
        })
        window.addEventListener("scroll", ()=>requestAnimationFrame(this.changeMargin));
    },
    unmounted(){
        window.removeEventListener("scroll", ()=>requestAnimationFrame(this.changeMargin));
    },
    computed:{

    },
    methods:{
        chooseImg(imageset){
            const len=imageset.length
            if(len==0){
                return ''
            }
            const r=Math.floor(Math.random()*len)
            return {
                'background-image': `url(${imageset[r].img})`
            }
        },
        changePage(dst){
            this.$router.push({name:dst})
        },
        jumpLink(){
            window.location.href='http://in.sducraft.top:8100'
        },
        changeMargin(){
            if(this.$route!='index'){
                window.removeEventListener("scroll", ()=>requestAnimationFrame(this.changeMargin));
            }
            const container = document.getElementById('Height');
            const scrollPosition = window.scrollY*0.5;
            const newHeight = Math.min(40 + scrollPosition, 330);
            container.style.marginTop = `${newHeight}px`; 
        }
    }
}
</script>

<style scoped>
.main {
    display: flex;
    margin: 0;
    padding: 0;
    height: 120vh;
    font-size: 1.1em;
}
.mianForMobile{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 0;
    padding: 0;
}
.aboutUs{
    margin: 50px 10%;
    width: 350px;
    height: 580px;
    background-color: #41728a;
    color: #ffffff;
    border-radius: 3px;
}
button {
    margin: 1em auto;
    width: 8em;
    height: 2.5em;
    border:0 solid #ffffff;
    background-color:#ffffff;
    font-size: 1.1em;
    color:#187ece;
    cursor: pointer;
    border-radius: 2px;
    transition: background-color 0.8s,border 0.8s;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
button:hover {
	border:1px solid #68b6ff;
    background-color:#68b6ff;
}
.main p{
    position: relative;
    z-index: 1;
    margin: 0.3em;
}
.description{
    text-align: center;
}
.description h1 {
    margin: 1em auto 0.5em auto;
	color: #d87d8f;
    font-size: 3em;

}
.description p {
	color: #ffffff;
	font-size: 1.3em;
    transition: color 0.8s;
}
.description button {
    margin-top: 18em;
    width: 8em;
    height: 3em;
    border:0 solid #1b8deb;
    background-color:#1b8deb;

    font-size: 1.2em;
    color:#fff;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.8s,border 0.8s;
}
.description button:hover {
	border:1px solid #68b6ff;
    background-color:#68b6ff;
}
.part{
    width: 100%;
    height: 500px;
}

.partbig,.partbig1,.partsmall,.partsmall1{
    display: inline-block;
    overflow: hidden;
    transition: background-color 0.8s;
    cursor: pointer;
    user-select: none;
    background-size: cover;
    position: relative;
    background-position:center center;
    transition: background-image 0.5s;
}
.partbig p,.partbig1 p,.partsmall p,.partsmall1 p{
    font-size: 24px;
}
.subbig,.subbig1,.subsmall,.subsmall1{
    width: 100%;
    height: 100%; 
    position:absolute; 
    top: 0;
    transition: background-color 0.8s;
}
.partsmall{
    width: 40%;
    height: 100%;
    background-color: #74bbd5;

}
.partbig{
    width: 60%;
    height: 100%;
    background-color: #8179b6;
}
.subbig{
    background-color: rgba(129, 121, 182, 0.8);
}
.subbig:hover{
    background-color: rgba(67, 63, 85, 0.7);
}
.partsmall1{
    width: 40%;
    height: 100%;
    background-color: #d6ac87;
}
.partbig1{
    width: 60%;
    height: 100%;
    background-color: #dc8a82;
    background-image: url('@/assets/images/map.png')
}
.subbig1{
    background-color: rgba(220, 138, 130, 0.8);
}
.subbig1:hover{
    background-color: rgba(57, 54, 78, 0.7);
}
.partbig:hover{
    background-color: #433f55;
}
.partbig1:hover{
    background-color: #39364e;
}
.partsmall:hover{
    background-color: #807a87;
}
.partsmall1:hover{
    background-color: #716c75;
}
@media screen and (max-width: 800px) {
.description button {
    margin-top: 8em;
}
.part{
    width: 100%;
    height: 160px;
}
.partbig p,.partbig1 p,.partsmall p,.partsmall1 p{
    font-size: 12px;
}
.subbig p:nth-child(1), .partsmall1 p:nth-child(1){
    margin: 18% 15% 0 15% !important;
}
button {
    margin: 1em 0 2em 1em;
    width: 8em;
    height: 2.5em;
    border:0 solid #ffffff;
    background-color:#ffffff;
    font-size: 1.1em;
    color:#187ece;
    cursor: pointer;
    border-radius: 2px;
    transition: background-color 0.8s,border 0.8s;
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
button:hover {
	border:1px solid #68b6ff;
    background-color:#68b6ff;
}
.aboutUsForMobile{
    width: 100%;
    background-color: #41728a;
    color: #ffffff;
    height:auto
}
}
</style>
