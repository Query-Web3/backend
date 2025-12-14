//go:generate go run ../tools/gqlgen.go

package gql

import (
	"context"

	"github.com/Query-Web3/backend/model"
	"github.com/vektah/gqlparser/v2/gqlerror"
)

type Resolver struct{}

func (r *Resolver) Query() QueryResolver {
	return &queryResolver{r}
}

type queryResolver struct{ *Resolver }

func (r *queryResolver) Txns(ctx context.Context, date *string, chain *string, asset *string, token *string, returnType *string, page int, size int) (string, error) {
	return "[]", nil
}

func (r *queryResolver) Yields(ctx context.Context, date *string, chain *string, asset *string, token *string, returnType *string, page int, size int) (*PageResult, error) {
	data, total, err := model.Yields(date, chain, asset, token, returnType, page, size)
	if err != nil {
		return nil, gqlerror.Errorf("Failed to get yields: %v", err)
	}

	return &PageResult{
		Total: int(total),
		Data:  data,
	}, nil
}
