(ns todo.core
  (:gen-class)
  (:require [clojure.string :as str]
            [ring.adapter.jetty :as jetty]
            [ring.util.response :as response]
            [ring.middleware.json :refer [wrap-json-body wrap-json-response]]
            [ring.middleware.params :refer [wrap-params]]
            [ring.middleware.resource :refer [wrap-resource]]
            [reitit.ring :as ring]
            [next.jdbc :as jdbc]
            [next.jdbc.result-set :as rs]
            [next.jdbc.sql :as sql])
  (:import [java.time Instant]
           [java.io File]))
 

(def db-spec {:dbtype "sqlite" :dbname "data/todos.db"})
(defonce datasource (delay (jdbc/get-datasource db-spec)))

(defn- ensure-data-dir! []
  (.mkdirs (File. "data")))

(defn init! []
  (ensure-data-dir!)
  (jdbc/execute! @datasource
                 ["CREATE TABLE IF NOT EXISTS todos (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     title TEXT NOT NULL,
                     completed INTEGER NOT NULL DEFAULT 0,
                     created_at TEXT NOT NULL
                   )"]))

(defn now [] (str (Instant/now)))

(defn list-todos []
  (sql/query @datasource
             ["SELECT id, title, completed, created_at
               FROM todos
               ORDER BY id DESC"]
             {:builder-fn rs/as-unqualified-lower-maps}))

(defn create-todo [title]
  (jdbc/execute-one! @datasource
                     ["INSERT INTO todos (title, completed, created_at)
      VALUES (?, ?, ?)
      RETURNING id, title, completed, created_at"
                      title false (now)]
                     {:builder-fn rs/as-unqualified-lower-maps}))

(defn get-todo [id]
  (jdbc/execute-one! @datasource
                     ["SELECT id, title, completed, created_at FROM todos WHERE id = ?" (long id)]
                     {:builder-fn rs/as-unqualified-lower-maps}))

(defn update-todo [id title completed?]
  (let [updates (cond-> {}
                  (some? title)      (assoc :title title)
                  (some? completed?) (assoc :completed (if completed? 1 0)))]
    (when (seq updates)
      (sql/update! @datasource :todos updates {:id (long id)}))
    [(get-todo id)]))

(defn delete-todo [id]
  (sql/delete! @datasource :todos {:id id}))


(defn- parse-int [x]
  (Integer/parseInt (str x)))

(def api-routes
  [["/" {:get {:handler (fn [_]
                          (-> (response/resource-response "index.html" {:root "public"})
                              (response/header "Cache-Control" "no-store")
                              (response/content-type "text/html")))}}]
   ["/api"
    ["/tasks"
     {:get {:handler (fn [_]
                       {:status 200
                        :headers {"Cache-Control" "no-store"}
                        :body (list-todos)})}
      :post {:handler (fn [{:keys [body]}]
                        (let [title (or (get body "title")
                                        (get body :title))]
                          (if (and title (not (str/blank? title)))
                            (let [row (create-todo title)]
                              {:status 201 :body row})
                            {:status 400 :body {:error "title is required"}})))}}]
    ["/tasks/:id"
     {:patch {:handler (fn [{:keys [path-params body]}]
                       (let [id (parse-int (:id path-params))
                             completed (or (get body "completed")
                                            (get body :completed)
                                            false)
                             title (or (get body "title")
                                        (get body :title))]
                         {:status 200 :body (update-todo id title completed)}))}
     :delete {:handler (fn [{:keys [path-params]}]
                          (delete-todo (parse-int (:id path-params)))
                          {:status 200 :body nil})}}]
                              ]])

(def app
  (-> (ring/ring-handler
       (ring/router api-routes)
       (ring/create-default-handler))
      (wrap-json-response)
      ;; Accept JSON request bodies; keep keys as-is to be permissive
      (wrap-json-body {:keywords? false})
      (wrap-params)
      ;; Serve files from resources/public at /
      (wrap-resource "public")))

(defn -main [& _]
  (init!)
  (println "Starting server on http://localhost:3000")
  (jetty/run-jetty app {:port 3000 :join? true}))
