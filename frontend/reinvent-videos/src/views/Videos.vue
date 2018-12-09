<template>
  <div>
    <div class="container" role="main">
      <h1 class="text-center title">re:Invent Videos.com</h1>
      <p class="text-center sub-title">
        A collection of
        <a
          href="https://reinvent.awsevents.com/"
          target="_blank"
          class="sub-title-link"
          >AWS re:Invent</a
        >
        videos and podcasts (when available) of past and current breakout
        sessions.
      </p>
      <p class="text-center text-muted">
        Built with <a href="https://vuejs.org" target="_blank">Vue.js</a>,
        <a href="https://serverless.com" target="_blank">Serverless Framework</a
        >, and powered by
        <a href="https://aws.amazon.com/" target="_blank">AWS</a> and
        <a href="https://www.algolia.com/" target="_blank">Algolia</a>.
        <a
          href="https://github.com/nragusa/reinventvideos"
          target="_blank"
          class="code-link"
          ><span class="far fa-code"></span
        ></a>
      </p>
      <ais-instant-search
        :search-client="searchClient"
        :index-name="index_by_views"
      >
        <ais-search-box
          placeholder="Search"
          :autofocus="true"
          :classNames="{
            'ais-SearchBox-input': 'form-control form-control-lg mb-2',
            'ais-SearchBox-submit': 'd-none',
            'ais-SearchBox-resetIcon': 'd-none',
            'ais-SearchBox-reset': 'd-none'
          }"
          :value="search"
        >
          <form action role="search" novalidate="novalidate">
            <div class="input-group input-group-lg mb-3">
              <div class="input-group-prepend">
                <button
                  class="btn dropdown-toggle btn-filter mb-2"
                  type="button"
                  data-toggle="collapse"
                  data-target="#filterDropdown"
                  aria-expanded="false"
                  aria-controls="filterDropdown"
                >
                  Filter
                </button>
              </div>
              <input
                type="search"
                autocorrect="off"
                autocapitalize="off"
                autocomplete="off"
                spellcheck="false"
                required="required"
                class="form-control"
                placeholder="Search"
                aria-label="Search"
                aria-describedby="button-addon1"
                v-model="search"
              />
            </div>
          </form>
        </ais-search-box>
        <div class="d-flex justify-content-end">
          <ais-powered-by
            theme="light"
            :classNames="{
              'ais-PoweredBy': 'mb-2 float-right'
            }"
          ></ais-powered-by>
        </div>
        <div class="row mb-3">
          <div class="col-12 col-md-4 mb-2">
            <div class="collapse" id="filterDropdown">
              <div class="card shadow">
                <h5 class="card-header">Sort By</h5>
                <div class="card-body">
                  <ais-sort-by
                    :items="[
                      {
                        value: index_by_views,
                        label: 'Views'
                      },
                      {
                        value: index_by_likes,
                        label: 'Likes'
                      }
                    ]"
                    :classNames="{
                      'ais-SortBy': 'mb-2',
                      'ais-SortBy-select': 'form-control'
                    }"
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="col-12 col-md-4 mb-2">
            <div class="collapse" id="filterDropdown">
              <div class="card shadow">
                <h5 class="card-header">Level</h5>
                <div class="card-body">
                  <ais-refinement-list attribute="level" :sortBy="sortBy">
                    <template slot="default" slot-scope="{ items, refine }">
                      <ul class="pl-2">
                        <li
                          v-for="item in items"
                          :key="item.value"
                          class="list-group-item refinementLists"
                        >
                          {{ item.value }}
                          <label class="switch">
                            <input
                              type="checkbox"
                              class="switch_1"
                              :value="item.value"
                              @change="refine(item.value)"
                              :checked="item.isRefined"/>
                            <span class="slider round"></span
                          ></label>
                          <span
                            class="float-right badge badge-pill badge-info"
                            >{{ item.count }}</span
                          >
                        </li>
                      </ul>
                    </template>
                  </ais-refinement-list>
                </div>
              </div>
            </div>
          </div>
          <div class="col-12 col-md-4 mb-2">
            <div class="collapse" id="filterDropdown">
              <div class="card shadow">
                <h5 class="card-header">Published Year</h5>
                <div class="card-body">
                  <ais-refinement-list
                    attribute="published_year"
                    :sortBy="sortBy"
                  >
                    <template slot="default" slot-scope="{ items, refine }">
                      <ul class="pl-2">
                        <li
                          v-for="item in items"
                          :key="item.value"
                          class="list-group-item refinementLists"
                        >
                          {{ item.value }}
                          <label class="switch">
                            <input
                              type="checkbox"
                              class="switch_1"
                              :value="item.value"
                              @change="refine(item.value)"
                              :checked="item.isRefined"/>
                            <span class="slider round"></span
                          ></label>
                          <span
                            class="float-right badge badge-pill badge-info"
                            >{{ item.count }}</span
                          >
                        </li>
                      </ul>
                    </template>
                  </ais-refinement-list>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="mx-auto">
            <ais-pagination
              :padding="2"
              :class-names="{
                'ais-Pagination': 'mb-3',
                'ais-Pagination-list': 'list-inline',
                'ais-Pagination-item': 'list-group-item pagination',
                'ais-Pagination-item--firstPage': 'pagination mr-1',
                'ais-Pagination-item--lastPage': 'pagination ml-1',
                'ais-Pagination-link': 'pagination-link',
                'ais-Pagination-item--disabled': 'pagination-disabled',
                'ais-Pagination-item--selected': 'pagination-selected'
              }"
            >
            </ais-pagination>
          </div>
        </div>
        <ais-hits>
          <template slot-scope="{ items }">
            <video-card :videos="items" />
          </template>
        </ais-hits>
        <div class="row">
          <div class="mx-auto">
            <ais-pagination
              :padding="2"
              :class-names="{
                'ais-Pagination': 'mt-4 mb-3',
                'ais-Pagination-list': 'list-inline',
                'ais-Pagination-item': 'list-group-item pagination',
                'ais-Pagination-item--firstPage': 'pagination mr-1',
                'ais-Pagination-item--lastPage': 'pagination ml-1',
                'ais-Pagination-link': 'pagination-link',
                'ais-Pagination-item--disabled': 'pagination-disabled',
                'ais-Pagination-item--selected': 'pagination-selected'
              }"
            >
            </ais-pagination>
          </div>
        </div>
      </ais-instant-search>
    </div>
    <Footer />
  </div>
</template>

<script>
import Footer from "@/views/Footer.vue";
import VideoCard from "@/components/VideoCard.vue";
import algoliasearch from "algoliasearch/lite";

export default {
  name: "VideoSearch",
  components: {
    VideoCard,
    Footer
  },
  data() {
    return {
      searchClient: algoliasearch(
        process.env.VUE_APP_ALGOLIA_APP,
        process.env.VUE_APP_ALGOLIA_API_KEY
      ),
      index_by_views: process.env.VUE_APP_ALGOLIA_INDEX_BY_VIEWS,
      index_by_likes: process.env.VUE_APP_ALGOLIA_INDEX_BY_LIKES,
      videos: [],
      sortBy: ["name:asc"],
      search: ""
    };
  }
};
</script>
<style scoped>
.code-link {
  color: #f59600;
}
</style>
