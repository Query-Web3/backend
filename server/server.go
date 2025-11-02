package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/handler/extension"
	"github.com/99designs/gqlgen/graphql/handler/transport"
	"github.com/99designs/gqlgen/graphql/playground"
	"github.com/go-chi/chi/v5"
	"github.com/go-chi/cors"

	gql "github.com/Query-Web3/backend/gql"
	"github.com/Query-Web3/backend/model"
)

func main() {
	// 创建路由
	router := chi.NewRouter()

	// 添加跨域中间件
	router.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"Accept", "Authorization", "Content-Type", "X-CSRF-Token"},
		ExposedHeaders:   []string{"Link"},
		AllowCredentials: false,
		MaxAge:           300,
	}))

	// initialize db connection
	model.InitializeDB()

	// initialize graphql server
	srv := handler.New(
		gql.NewExecutableSchema(gql.Config{Resolvers: &gql.Resolver{}}),
	)
	srv.AddTransport(transport.GET{})
	srv.AddTransport(transport.POST{})
	srv.Use(extension.Introspection{})

	// add graphql handler
	router.Handle("/", playground.Handler("web3query", "/gql"))
	router.Handle("/gql", srv)

	port := 8082
	if IsFileExists("./ssl/ser.pem") && IsFileExists("./ssl/ser.key") {
		log.Printf("connect to https://0.0.0.0:%s/ for GraphQL playground", fmt.Sprint(port))
		http.ListenAndServeTLS(":"+fmt.Sprint(port), "./ssl/ser.pem", "./ssl/ser.key", router)
	} else {
		log.Printf("connect to http://0.0.0.0:%s/ for GraphQL playground", fmt.Sprint(port))
		http.ListenAndServe(":"+fmt.Sprint(port), router)
	}
}

func IsFileExists(filename string) bool {
	_, err := os.Stat(filename)
	if err != nil {
		if os.IsNotExist(err) {
			return false
		}
	}
	return true
}
