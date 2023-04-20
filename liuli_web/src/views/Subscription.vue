<template>
  <div class="app-content bg-white">
    <div class="flex justify-between px-5 pt-5">
      <div class="ml-20">
        <el-select v-model="selectData.doc_source_items" placeholder="选择订阅源" size="default" @change="onDocSourceSelect">
          <el-option v-for="item in selectData.doc_source_options" :key="item.value" :label="item.label"
            :value="item.value" />
        </el-select>
      </div>
      <div class="mr-5">
        <el-button type="primary" class="el-icon--right" size="default" @click="subSearch">
          搜索<el-icon class="el-icon--right">
            <Right />
          </el-icon></el-button>
      </div>
    </div>
    <!-- <main class="main-content">
      <div class="search-bar" role="list">
        <div class="search-bar-left">
          <div>
            <multi-select :options="selectData.doc_source_options" :selected-options="selectData.doc_source_items"
              placeholder="选择订阅源" @select="onDocSourceSelect">
            </multi-select>
          </div>
        </div>
        <div class="search-bar-right">
          <button aria-busy="false" type="submit" class="outline contrast sub-search" @click="subSearch()">
            搜索
            <span style="display: inherit; margin-right: -4px; margin-left: 8px">
              <svg style="
                  user-select: none;
                  width: 1em;
                  height: 1em;
                  display: inline-block;
                  fill: currentcolor;
                  flex-shrink: 0;
                  transition: fill 200ms;
                " focusable="false" aria-hidden="true" viewBox="0 0 24 24" data-testid="ArrowForwardOutlinedIcon">
                <path d="m12 4-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8-8-8z"></path>
              </svg>
            </span>
          </button>
        </div>
      </div>
    </main> -->
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { UserStore, useUserStore } from '@/store/user';
import { userApi } from '@/api';
import { ElNotification } from 'element-plus';
import { Right } from '@element-plus/icons-vue';
// import { MultiSelect } from 'vue-search-select';
// import 'vue-search-select/dist/VueSearchSelect.css';

const collapsed = ref(false);
const title = ref('我的订阅');

const selectData = ref({
  doc_source_options: [],
  doc_source_items: [],
  doc_source_author_items: []
});

console.log(selectData.value.doc_source_options);

function onDocSourceSelect(items: never[], lastSelectItem: any) {
  selectData.value.doc_source_items = items;
  console.log(selectData.value.doc_source_items);
}

function menuStatus(value: boolean) {
  // 获取导航栏传递过来的状态值
  collapsed.value = value;
}

function subSearch() {
  console.log(selectData.value.doc_source_items[0]);
}

onMounted(() => {
  const userStore = UserStore();
  // userApi
  //   .getStats({
  //     username: userStore.username
  //   })
  //   .then((res) => {
  //     if (res.status == 200) {
  //       console.log(res);
  //       // 有结果表示正常请求
  //       // 开始处理数据
  //       for (var key in res.data.doc_source_stats_dict) {
  //         // 生成订阅源 select 数据
  //         selectData.value.doc_source_options.push({
  //           value: key,
  //           text: res.data.doc_source_stats_dict[key].doc_source_alias_name
  //         });
  //       }
  //       selectData.value.doc_source_items = selectData.value.doc_source_options;
  //     } else {
  //       const msg = res.info ? res.info : '服务器超时';
  //       ElNotification({
  //         message: msg,
  //         type: 'error',
  //         duration: 2000
  //       });
  //     }
  //   });
});
</script>

<style lang="scss" scoped>
:deep(input) {
  margin-bottom: 0 !important;
  padding: 0 !important;
  height: 1.5rem;
  width: 300px !important;
}

input:not([type='checkbox'], [type='radio'], [type='range']) {
  height: auto;
}

.ui.multiple.search.dropdown>.text {
  font-size: 15px;
  /* margin-top: 0.6em; */
}

.ui.multiple.dropdown>.label {
  /* margin-top: 0.35em; */
  color: rgb(255, 255, 255);
  background-color: #b9b9b9;
  text-decoration: none;
  box-shadow: rgb(220 214 214 / 20%) 0px 3px 1px -2px, rgb(180 173 173 / 14%) 0px 2px 2px 0px,
    rgb(213 203 203 / 12%) 0px 1px 5px 0px;
}

.ui.selection.dropdown {
  /* height: 40px;
  line-height: 40px; */
  border: 0px;
  box-shadow: rgb(220 214 214 / 20%) 0px 3px 1px -2px, rgb(180 173 173 / 14%) 0px 2px 2px 0px,
    rgb(213 203 203 / 12%) 0px 1px 5px 0px;
}
</style>

<style scoped>
.main-content {
  margin-left: 30px;
  margin-right: 30px;
  /* margin-top: 30px; */
}

div.search-bar {
  width: 100%;
  /* height: 40px; */
}

div.search-bar .search-bar-left {
  float: left;
  /* width: 420px; */
}

div.search-bar .search-bar-right {
  float: right;
}

div.search-bar-right .sub-search {
  margin-bottom: auto !important;
  width: 100px;
  font-size: 15px;
  /* height: 39px; */
  /* line-height: 40px; */

  display: inline-flex;
  -webkit-box-align: center;
  align-items: center;
  -webkit-box-pack: center;
  justify-content: center;
  position: relative;
  box-sizing: border-box;
  -webkit-tap-highlight-color: transparent;
  outline: 0px;
  border: 0px;
  cursor: pointer;
  user-select: none;
  vertical-align: middle;
  appearance: none;
  text-decoration: none;
  font-family: Inter, Helvetica, Arial, sans-serif;
  font-weight: 500;
  /* font-size: 0.875rem; */
  /* line-height: 1.7; */
  text-transform: uppercase;
  min-width: 64px;
  padding: 6px 16px;
  border-radius: 4px;
  color: rgb(255, 255, 255);
  background-color: rgb(67, 129, 255);
  transition: background-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
    box-shadow 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
    border-color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms,
    color 250ms cubic-bezier(0.4, 0, 0.2, 1) 0ms;

  box-shadow: rgb(0 0 0 / 20%) 0px 3px 1px -2px, rgb(0 0 0 / 14%) 0px 2px 2px 0px,
    rgb(0 0 0 / 12%) 0px 1px 5px 0px;
}

div.search-bar-right .sub-search:hover {
  text-decoration: none;
  background-color: rgb(46, 90, 178);
  box-shadow: 0px 2px 4px -1px rgb(0 0 0 / 20%), 0px 4px 5px 0px rgb(0 0 0 / 14%),
    0px 1px 10px 0px rgb(0 0 0 / 12%);
}
</style>
