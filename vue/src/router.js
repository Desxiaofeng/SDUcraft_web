import { createRouter, createWebHistory } from "vue-router";
import routeData from "./routedata.json"

const routes=[]

routeData.forEach(route => {
    //第一级
    if(route.type=='nav'){
        routes.push({
            path: route.path,
            name: route.routeName,
            component: () => import(`./body/${route.component}.vue`)
        })
    }
    //第二级
    if(route.children.length>0){
        route.children.forEach(child_route =>{
            if(child_route.type=='nav'){
                routes.push({
                    path: child_route.path,
                    name: child_route.routeName,
                    component: () => import(`./body/${child_route.component}.vue`)
                })
            }
            //第三级
            if(child_route.children && child_route.children.length>0){
                child_route.children.forEach(child_child_route=>{
                    if(child_child_route.type=='inline'){
                        routes.push({
                            path: child_child_route.path,
                            name: child_child_route.routeName,
                            component: () => import(`./body/${child_child_route.component}.vue`)
                        })
                    }
                })
            }
            
        })
    }
})
//404
routes.push({
    path: '/404',
    name: 'NotFound',
    component:()=>import('./body/BodyNotFound.vue')
})
routes.push({
    path: '/:pathMatch(.*)*',
    redirect: '/404'
})


const router=createRouter(
    {
        history: createWebHistory(),
        routes,
        scrollBehavior(to, from, savedPosition) {
            //特殊处理notice
            if(to.name=='notice' && from.name=='notice'){
                return null
            }
            //一般逻辑
            if (savedPosition) {
              return savedPosition; // 返回上次滚动位置
            }
            return { top: 0 }; // 默认滚动到顶部
          },
    }
);

export default router;