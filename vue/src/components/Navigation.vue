<template>
    <nav>
        <router-link :to="route.path" v-for="route in routeData" class="navItem" @click="hideItem">
            <p class="navItemP" >{{ route.name }}</p>
            <router-link :to="childRoute.path" v-for="childRoute in route.children" :style="isClick" class="navItemDropdownContent"  @click.stop="hideItem">
                <p class="navItemDropdownContentP">{{ childRoute.name }}</p>
            </router-link>
        </router-link>
    </nav>
</template>

<script>
import routeData from "../routedata.json"

export default {
    data() {
        return {
            routeData,
            isClick:{
                display:''
            }
        }
    },
    methods: {
        hideItem(){
            this.isClick.display='none'

            setTimeout(() => {
                this.isClick.display=''
            }, 10);

        }
    },
    created() {

    },
}
</script>

<style scoped>
nav {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;

    height: 56px;
    background-color: rgb(88, 181, 243);
}

.navItem {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;

    height: 100%;
    width: 128px;
    display: inline;
}

.navItemP {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;

    height: 100%;
    font-size: 1.4em;
    text-align: center;
    color: #ffffff;
}

.navItem:hover .navItemP {
    background-color: #87c9f4;
}

.navItemDropdownContent {
    display: none;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;

    background-color: rgb(0, 145, 255);
    width: inherit;
    height: 80%;
    position: relative;
    z-index: 10;

}

.navItemDropdownContentP {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0;
    padding: 0;

    height: 100%;
    font-size: large;
    text-align: center;
        color: #ffffff;
}

.navItem:hover .navItemDropdownContent {
    display: block;
}

.navItemDropdownContent:hover .navItemDropdownContentP {
    background-color: rgb(135, 201, 244);
}

a{
    text-decoration: none;
    color: inherit;
}
.router-link-active{
    background-color: #0479ff;
}
a:has(.router-link-active){
    background-color: #0479ff;
}


* {
    overflow: visible;
    /* word-wrap: break-word; */
    /* overflow-wrap: break-word; */
    /* white-space: pre-wrap; */
}
</style>
