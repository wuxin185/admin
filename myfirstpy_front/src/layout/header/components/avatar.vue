<template>
    <el-dropdown>
        <span class="el-dropdown-link">
            <el-avatar :size="40" :src="squareUrl" />
            &nbsp;&nbsp;{{ currentUser.username }}
            <el-icon class="el-icon--right">
                <arrow-down />
            </el-icon>
        </span>
        <template #dropdown>
            <el-dropdown-menu>
                <el-dropdown-item>
                    <router-link :to="{ name: '个人中心' }">个人中心</router-link>
                </el-dropdown-item>
                <el-dropdown-item @click="logout">安全退出</el-dropdown-item>
            </el-dropdown-menu>
        </template>
    </el-dropdown>
</template>
<script setup>
import store from '@/store'
import router from '@/router';
import { getServerUrl } from '@/util/request';
import { ArrowDown } from '@element-plus/icons-vue'

const currentUser = JSON.parse(sessionStorage.getItem("currentUser"))

const squareUrl = getServerUrl() + 'media/userAvatar/' + currentUser.avatar

console.log(squareUrl)

const logout = () => {
    // window.sessionStorage.clear()
    store.commit("RESET_TABS")
    router.replace('/login')
}
</script>
<style lang="scss" scoped>
.el-dropdown-link {
    cursor: pointer;
    color: var(--el-color-primary);
    display: flex;
    align-items: center;
}
</style>