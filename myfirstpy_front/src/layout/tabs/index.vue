<template>
    <el-tabs v-model="editableTabsValue" type="card" class="demo-tabs" closable @tab-remove="removeTab"
        @tab-click="clickTab">
        <el-tab-pane v-for="item in editableTabs" :key="item.name" :label="item.title" :name="item.name">
        </el-tab-pane>
    </el-tabs>
</template>

<script setup>
import { ref, watch } from 'vue'
import store from '@/store'
import { useRouter } from 'vue-router';

const router = useRouter()

const editableTabsValue = ref(store.state.editableTabsValue)
const editableTabs = ref(store.state.editableTabs)


const removeTab = (targetName) => {
    const tabs = editableTabs.value
    let activeName = editableTabsValue.value
    if (activeName === '/index') {
        return
    }
    if (activeName === targetName) {
        tabs.forEach((tab, index) => {
            if (tab.name === targetName) {
                const nextTab = tabs[index + 1] || tabs[index - 1]
                if (nextTab) {
                    activeName = nextTab.name
                }
            }
        })
    }
    router.push({ path: activeName })

    editableTabsValue.value = activeName
    editableTabs.value = tabs.filter((tab) => tab.name !== targetName)


    store.state.editableTabsValue = editableTabsValue.value
    store.state.editableTabs = editableTabs.value
}

const refreshTabs = () => {
    editableTabs.value = store.state.editableTabs
    editableTabsValue.value = store.state.editableTabsValue
}

watch(store.state, () => {
    refreshTabs();
}, { deep: true, immediate: true })

const clickTab = (target) => {
    router.push({ name: target.props.label })
}
</script>

<style scoped>
.demo-tabs>.el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}

.el-tabs--card>.el-tabs__header .el-tabs__item.is-active {
    background-color: lightgray;
}

.el-main {
    padding: 0px;
}

.el-tabs__content {
    padding: 0px !important;
    ;
}
</style>