//go:generate go run ../tools/gqlgen.go

package gql

import (
	"context"

	"github.com/Query-Web3/backend/model"
	"github.com/vektah/gqlparser/v2/gqlerror"
)

type Resolver struct{}

// func (r *Resolver) Customer() CustomerResolver {
// 	return &customerResolver{r}
// }

// func (r *Resolver) Order() OrderResolver {
// 	return &orderResolver{r}
// }

func (r *Resolver) Query() QueryResolver {
	return &queryResolver{r}
}

type queryResolver struct{ *Resolver }

func (r *queryResolver) Txns(ctx context.Context, date *int, chain *int, asset *string, token *string, returnType *string) (string, error) {
	return "[]", nil
}

func (r *queryResolver) Yields(ctx context.Context, date *int, chain *int, asset *string, token *string, returnType *string) (string, error) {
	data, err := model.Yields()
	if err != nil {
		return "", gqlerror.Errorf("Failed to get yields: %v", err)
	}

	return data, nil
}
