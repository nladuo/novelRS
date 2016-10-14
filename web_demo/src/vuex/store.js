/**
 * Created by kalen on 10/11/16.
 */

import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const state = {
  novels: []
};

const mutations = {
  SEARCH_NOVELS (state, name) {
    let url = '/api/search/' + name;
    $.ajax({
      type: "GET",
      url: url,
      dataType: "json",
      success: (data) => {
        state.novels = data;
        if (data.length == 0){
          alert("未找到" + name);
        }
      }
    });
  }
};


export default new Vuex.Store({
  state,
  mutations
});
