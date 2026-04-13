import {createRouter,createWebHistory} from 'vue-router'
import Home from './components/HomePage'
import Admin from './components/AdminPage'
import Login  from './components/LoginPage'
import Signup  from './components/SignupPage'
import Cart  from './components/ShoppingCart'
import Manager  from './components/ManagerPage'
import Product from './components/ProductPage'
import ItemTask from './components/ItemTasks'
import ItemUpdate from './components/ItemUpdate'
import CategoryAdd from './components/CategoryAdd'
const routes = [
    {
        path:'/',
        name:'home',
        component:Home
    },
    {
        path:'/admin',
        name:'admin',
        component:Admin
    },
    {
        path:'/login',
        name:'login',
        component:Login
    },
    {
        path:'/signup',
        name:'signup',
        component:Signup
    },
    {
        path:'/cart',
        name:'cart',
        component:Cart
    },
    {
        path:'/manager',
        name:'manager',
        component:Manager
    },
    {
        path:'/product/:id',
        name:'product',
        component:Product,
        props: true
    },
    {
        path:'/itemtask/:id',
        name:'itemtask',
        component:ItemTask,
        props: true
    },
    {
        path:'/itemupdate/:id',
        name:'itemupdate',
        component:ItemUpdate,
        props: true
    },
    {
        path:'/catadd',
        name:'catupdate',
        component:CategoryAdd,
    },
]

const router = createRouter({
    history:createWebHistory(),
    routes,
})
/*router.beforeEach((to,from,next) =>{
    if((to.name !== 'login') && !localStorage.getItem('auth-token') ? true : false)
      next({ name : 'login'})
    else next()
  })*/

export default router;
