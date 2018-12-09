<template>
  <div class="card-deck">
    <div class="card mb-3 shadow" v-for="item in videos" :key="item.objectID">
      <a :href="'https://www.youtube.com/watch?v=' + item.vid" target="_blank">
        <img class="card-img-top" :src="item.thumbnail" alt="Session Preview" />
      </a>
      <div class="card-body">
        <h5 class="card-title">
          <ais-highlight :hit="item" attribute="title"></ais-highlight>
        </h5>
        <a
          :href="'https://www.youtube.com/watch?v=' + item.vid"
          target="_blank"
        >
          <span class="fab fa-youtube fa-2x icon-link"></span>
        </a>
        <a :href="item.podcast" v-if="item.podcast">
          <span class="far fa-podcast fa-2x pl-2 icon-link"></span>
        </a>
        <span class="float-right">{{ item.views }} views </span>
        <p class="card-text">
          <ais-highlight :hit="item" attribute="description"></ais-highlight>
        </p>
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">
          <span class="fas fa-heart mr-1"></span>{{ item.likes }}
          <span class="float-right">{{ item.level }}</span>
          <span
            class="fas fa-layer-group mr-1 mt-1 float-right"
            v-if="item.level"
          ></span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: "VideoCard",
  props: {
    videos: Array,
    start: Number
  }
};
</script>

<style scoped></style>
