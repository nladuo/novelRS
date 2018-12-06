<template>
  <table class="table table-striped table-bordered">
    <thead>
      <tr>
        <td>书名</td>
        <td>作者</td>
        <td>分类</td>
        <td>相似度</td>
      </tr>
    </thead>
    <tbody>
      <tr v-for="novel in novels">
        <td>{{ novel.name }}</td>
        <td>{{ novel.author }}</td>
        <td>{{ novel.category }}</td>
        <td>{{ convert(novel.similarity) }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
  import {getNovels} from '../vuex/getters'
  export default {
    methods: {
      convert(similarity){
        return Math.floor(similarity * 10000) / 100 + '%';
      }
    },
    vuex: {
      getters: {
        novels: getNovels
      }
    }
  }
</script>
