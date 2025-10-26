package main

import (
	"log"
	"net/http"

	"github.com/99designs/gqlgen/graphql/handler"
	"github.com/99designs/gqlgen/graphql/handler/extension"
	"github.com/99designs/gqlgen/graphql/handler/transport"
	"github.com/99designs/gqlgen/graphql/playground"

	gql "github.com/Query-Web3/backend/gql"
	"github.com/Query-Web3/backend/model"
)

func main() {
	router := http.NewServeMux()

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

	log.Println("connect to http://localhost:8082/ for graphql playground")
	log.Fatal(http.ListenAndServe(":8082", router))
}
