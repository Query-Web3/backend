package model

import (
	"encoding/json"

	db "github.com/Query-Web3/backend/model/dbgen"
)

func Yields() (string, error) {
	users := []db.BifrostSiteTable{}
	result := DB.Find(&users)
	if result.Error != nil {
		return "", result.Error
	}

	jsonStr, err := json.Marshal(users)
	if err != nil {
		return "", err
	}
	return string(jsonStr), nil
}

type YieldItem struct {
	Token string  `json:"token"`
	Apy   float64 `json:"apy"`
	Tvl   float64 `json:"tvl"`
	Price float64 `json:"price"`
}
