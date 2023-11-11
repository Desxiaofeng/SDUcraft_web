<template>
    <div class="mainLayout">
        <n-result v-if="random<0.33" style="padding-top: 10em;" status="404" title="404 资源不存在" description="生活总归带点荒谬">
            <template #footer>
            <n-button @click="jumpLink">找点乐子吧</n-button>
            </template>
        </n-result>
        <n-result
            v-else-if="random<0.66"
            style="padding-top: 10em;"
            status="403"
            title="403 禁止访问"
            description="总有些门是对你关闭的"
        >
            <template #footer>
            <n-button @click="jumpLink">放轻松</n-button>
            </template>
        </n-result>
        <n-result
            v-else
            style="padding-top: 10em;"
            status="403"
            title="403 禁止访问"
            description="这是不能碰的滑梯"
        >
            <template #footer>
            <n-button @click="jumpLink">放轻松</n-button>
            </template>
        </n-result>
    </div>
    </template>
    
    <script>
    export default{
        data(){
            return{
                random:null,
                websites:[
                    "https://ys.mihoyo.com/",
                    "https://www.minecraft.net/",
                    "http://in.sducraft.top",
                    "https://www.sdu.edu.cn",
                    "https://www.bilibili.com"
                ]
            }
        },
        mounted(){
            this.random=Math.random()
        },
        methods:{
            jumpLink(){
                const r=Math.floor(Math.random()*5)
                window.location.href=this.websites[r]
            }
        }
    }
    </script>
    
    <style scoped>
    .mainLayout{
        margin: 0 18%;
        min-height: 83vh;
        background-color: #ffffff;
    }
    @media screen and (max-width: 800px) {
        .mainLayout{
        margin: 0;
        min-height: 83vh;
        }
    }
    </style>