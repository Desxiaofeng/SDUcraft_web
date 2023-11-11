<template>
    <el-menu
    v-if="!ismobile"
    :default-active="this.$route.path"
    mode="horizontal"
    :ellipsis="false"
    :router="true"
    :style="{boxShadow: `var(--el-box-shadow-lighter)`}"
    :show-timeout=0
    :hide-timeout=0
    menu-trigger="hover"
    :unique-opened="true"
    >
    <div  class="navLeft1">
    <a href="/" style="padding: 0 0.5em;">
        SDUcraft
    </a>
    </div>
    <div class="flex-grow" />
    
    <template v-for="route in routeData">
        <el-menu-item v-if="route.type=='nav'" :index="route.path">{{ route.name }}</el-menu-item>
        <el-sub-menu v-if="route.type=='menu'" :index="route.path">
            <template #title>{{ route.name }}</template>
            <template v-for="subRoute in route.children">
                <el-menu-item v-if="subRoute.type=='nav'" :index="subRoute.path">{{ subRoute.name }}</el-menu-item>
                <el-menu-item v-if="subRoute.type=='link'" @click="jumpLink(subRoute.url)"
                >
                    {{ subRoute.name }}
                </el-menu-item>
            </template>
        </el-sub-menu>
    </template>
    </el-menu>

    <!-- for mobile -->
    <div class="mobileNav" v-if="ismobile">
        <div v-if="!isNotice" class="navLeft1" >
            <a href="/" title>SDUcraft</a>
        </div>
        <div v-else class="navLeft2" @click="changeNoticeBar">
            <el-icon style="display:inline-block;margin: auto;" size="32"><i-ep-Expand /></el-icon><span style="margin: auto;">Notice List</span>
        </div>
        <div @click="openMenu" class="navRight">
            <el-icon style="display:inline-block" size="32"><i-ep-Menu /></el-icon>MENU
        </div>
    </div>
    <div class="navDown" :style="navDownOpen">
        <div v-for="route in routeData" :style="displayStyle()">

            <div v-if="route.type=='menu'" class="navDownContent">
                <div class="navDownContentHeader"  @click="openSubMenu(route)">
                    {{ route.name }}
                    <el-icon><i-ep-CaretBottom /></el-icon>
                </div>
                <div class="navDownContentContent" :style="navDownContentContentOpen(route)">
                    <div v-for="subRoute in route.children" :style="subDisplayStyle(route)">
                        <router-link v-if="subRoute.type=='nav'" :to="subRoute.path" class="subItem" @click="openMenu">
                            {{ subRoute.name }}
                        </router-link>
                        <a v-if="subRoute.type=='link'" :href="subRoute.url" class="subItem" @click="openMenu">
                            {{ subRoute.name }}
                        </a>
                    </div>
                </div>

            </div>
            <router-link v-if="route.type=='nav'" :to="route.path" class="navDownContent" @click="openMenu">
                <div class="navDownContentHeader">
                    {{ route.name }}
                    <div></div>
                </div>
            </router-link>
            <a v-if="route.type=='link'" class="navDownContent" @click="openMenu">
                <div class="navDownContentHeader">
                    {{ route.name }}
                    <div></div>
                </div>
            </a>

        </div>
    </div>


</template>
  
<script>
import routeData from "../routedata.json"
  
export default {
    data() {
        return {
            routeData,
            isopen:false,
            isdisplay:false,
            isSubDisplay:{},
            subChoice:null,
            navDownOpen:{height:0}
        }
    },
    props:['isNotice','ismobile'],
    emits:['changeNoticeBar'],
    methods: {
        jumpLink(url){
            window.location.href=url
        },
        openMenu(){
            if(!this.isopen){
                this.isopen=true
                this.navDownOpen={height:'254px'}
                setTimeout(()=>{
                    this.isdisplay=true
                },250)
            }else{
                setTimeout(()=>{
                    this.isdisplay=false
                },250)
                this.isdisplay=false
                this.isopen=false
                this.routeData.forEach(route_=>{
                this.isSubDisplay[route_.routeName]=false
                })
                this.subChoice=null
                this.navDownOpen={height:'0'}
            }
        },
        displayStyle(){
            if(this.isdisplay){
                return {
                    'display':'block'
                }
            }else{
                return {
                    'display':'none'
                }
            }
        },
        openSubMenu(route){
            this.routeData.forEach(route_=>{
                this.isSubDisplay[route_.routeName]=false
            })
            if(this.subChoice==route){
                this.subChoice=null
                this.navDownOpen={height:'254px'}
            }else{
                this.subChoice=route
                const heightValue=254+route.children.length*40
                this.navDownOpen={height: heightValue+'px'}
                setTimeout(()=>{
                    this.isSubDisplay[route.routeName]=true
                },250)
            }
        },
        subDisplayStyle(route){
            if(this.isSubDisplay[route.routeName]){
                if(this.subChoice==route){
                    return {
                        'display':'block'
                    }
                }else{
                    return {
                        'display':'none'
                    }
                }
            }else{
                return {
                        'display':'none'
                    }
            }
        },
        navDownContentContentOpen(route){
            if(this.subChoice==route){
                const heightValue=40*route.children.length
                return {
                    height: heightValue+'px'
                }
            }else{
                return {
                    height:'0'
                }
            }
        },
        changeNoticeBar(){
            this.$emit("changeNoticeBar")
        }
    },
    watch:{
        routeData(){
            this.isSubDisplay={}
            this.routeData.forEach(route=>{
                this.isSubDisplay[route.routeName]=false
            })
        }
    }
}
</script>

<style scoped>
/* 下面俩用来修复elementplus bug */
.el-menu--horizontal .el-menu-item:not(.is-disabled):focus{
    outline: 0;
    color:#303133;
    background-color: #ffffff;
}
.el-menu--horizontal .el-menu-item:not(.is-disabled):hover {
    outline: 0;
    color: var(--el-menu-hover-text-color);
    background-color: var(--el-menu-hover-bg-color);
}
.flex-grow {
flex-grow: 1;
}
.mobileNav{
    height:60px;
    width: 100%;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #cccccc;
}
.mobileNav div:active{
    background-color: #cccccc;
}
.navLeft1 a{
    color: rgb(199, 81, 81);
    text-decoration: none;
    height: 100%;
    display: inline-flex;
    align-items: center;
    font-size: 1.5em;
    cursor: pointer;
    user-select: none;
}
.navLeft2{
    display: flex;
    flex-direction: row;
    text-align: center;
    padding: 0 1em;
    cursor: pointer;
    user-select: none;
}

.navRight{
    display: flex;
    align-items: center;
    padding: 0 1em;
    cursor: pointer;
    user-select: none;
}
.navDown{
    width: 100%;
    height: 0;
    background-color: #fafafa;
    transition: all 0.3s;
}
.navDownContent{
    min-height: 50px;
    text-decoration: none;
    color: #000000;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.navDownContentHeader{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 1em;
    height: 50px;
    border-bottom: 1px solid #d6d6d6;
    cursor: pointer;
    user-select: none;
}
.navDownContentHeader:active{
    background-color: #cccccc;
}
.navDownContentContent{
    height: 0;
    transition: all 0.3s;
}
.subItem{
    height: 40px;
    border-bottom: 1px solid #dddddd;
    text-decoration: none;
    color: #000000;
    background-color: #fafafa;
    display: flex;
    align-items: center;
    padding: 0 2em;
}
.subItem:active{
    background-color: #cccccc;
}
</style>
  