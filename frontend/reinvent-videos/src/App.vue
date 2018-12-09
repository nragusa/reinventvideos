<template>
  <div id="app"><router-view /></div>
</template>

<style>
html {
  position: relative;
  min-height: 100%;
}
body {
  font-size: 0.875rem;
  background-color: #fff;
}

[role="main"] {
  padding-top: 55px;
  padding-bottom: 60px;
}

.feather {
  width: 16px;
  height: 16px;
  vertical-align: text-bottom;
}
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 60px;
  line-height: 55px;
  background-color: #4484ce;
}
.navbar .form-control {
  padding: 0.75rem 1rem;
  border-width: 0;
  border-radius: 0;
}
.nav {
  background: #4484ce !important;
}
.logo {
  color: #f59600;
  font-size: 2em;
}
.nav-link {
  color: #f59600;
  font-size: 1.5em;
}
.nav-link:hover {
  color: #0b4fa1;
  font-size: 1.5em;
}
.title {
  font-family: "Indie Flower";
  color: #f59600;
  font-size: 4em;
}
.sub-title {
  font-size: 1.3em;
}
.sub-title-link {
  color: #f59600;
}
.btn-filter {
  color: #fff;
  background-color: #0b4fa1;
  border: 0px;
}
.btn-filter:hover {
  color: #fff;
  background-color: #4484ce;
  border: 0px;
}
.btn-filter:active {
  background-color: #4484ce;
  border: 0px;
}
.badge-info {
  background-color: #0b4fa1;
}
.card-header {
  background-color: #4484ce;
  color: #fff;
  border-bottom: 0;
}
.refinementLists {
  padding: 0.2rem;
  border: 0px;
  font-size: 1.3em;
}
.dropdown-item.active {
  background-color: #4484ce;
}
.dropdown-item:active {
  background-color: #4484ce;
}
.pagination {
  border: 0;
  padding: 0.5rem 0.75rem;
}
.pagination-link {
  color: #0b4fa1;
  font-size: 1.2em;
}
.pagination-link:hover {
  color: #4484ce;
}
.pagination-disabled {
  color: #f7f9fb !important;
  background-color: #f7f9fb;
}
.pagination-selected {
  color: #f59600 !important;
  background-color: #f59600;
}
.icon-link {
  color: #0b4fa1;
}
.icon-link:hover {
  color: #4484ce;
}
.social-icons {
  color: #0b4fa1;
  font-size: 2em;
}
</style>
