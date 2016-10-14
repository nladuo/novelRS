<template>
  <div class="form-group">
    <div class="input-group">
      <input v-model="novel_name" type="text" class="form-control" placeholder="请输入小说名称"/>
      <div class="input-group-btn">
        <button @click="search" class=" btn btn-primary btn-block">搜索类似小说</button>
      </div>
    </div>
  </div>
</template>

<script>
  import {searchNovels} from '../vuex/actions'
  export default {
    data() {
      return {
        novel_name: ""
      }
    },
    vuex: {
      actions: {
        searchNovels
      }
    },
    methods: {
      search() {
        this.searchNovels(this.novel_name)
      }
    }
  }
</script>
