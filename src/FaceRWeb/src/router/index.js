import Vue from 'vue'
import Router from 'vue-router'
//  import HelloWorld from '@/components/HelloWorld'

const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/camera', component: 'Camera'}
]

//  Vue.use(Router)
//
//  export default new Router({
//    routes: [
//      {
//        path: '/',
//        name: 'HelloWorld',
//        component: HelloWorld
//      }
//    ]
//  })

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

export default new Router({
  routes,
  mode: 'history'
})
