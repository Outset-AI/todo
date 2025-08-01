(defproject clojure-todo-web "0.1.0-SNAPSHOT"
  :description "A web server-based to-do list application"
  :url "http://example.com/clojure-todo-web"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.12.1"]
                 [ring "1.9.3"]
                 [ring/ring-json "0.5.0"]
                 [ring/ring-defaults "0.3.4"]
                 [compojure "1.6.2"]
                 [org.clojure/core.async "1.6.681"]
                 [http-kit/http-kit "2.8.0"]
                 [metosin/reitit "0.7.1"]
                 [org.xerial/sqlite-jdbc "3.45.3.0"]
                 [com.github.seancorfield/next.jdbc "1.3.925"]
                 [hiccup "2.0.0"]]
  :main todo.core
  :resource-paths ["resources"]
  :profiles {:dev {:dependencies [[ring/ring-mock "0.3.2"]]}})
