<template>
  <table class="table table-bordered">
    <thead>
      <tr>
        <td>书名</td>
        <td>作者</td>
        <td>分类</td>
        <td>字数</td>
        <td>相似度</td>
      </tr>
    </thead>
    <tbody>
      <tr v-for="novel in novels">
        <td>{{ novel.name }}</td>
        <td>{{ novel.author }}</td>
        <td>{{ novel.category }}</td>
        <td>{{ novel.word_num }}</td>
        <td>{{ novel.similarity }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import {getNovels} from '../vuex/getters'
  export default {
    vuex: {
      getters: {
        novels: getNovels
      }
    }
  }
</script>
