package model

import (
	"encoding/json"
	"time"
)

// CREATE TABLE token_ext (
//     chain VARCHAR(32) NOT NULL COMMENT 'Chain Name',
//     token VARCHAR(255) NOT NULL COMMENT 'Primary Key',
//     type VARCHAR(50) COMMENT 'Asset Type',
//     return_type VARCHAR(50) COMMENT 'Return Type',
//     PRIMARY KEY (chain, token)
// ) COMMENT 'Table to store extended token information';

func Yields(date *string, chain *string, asset *string, token *string, returnType *string, page, size int) (string, int64, error) {
	if page < 1 {
		page = 1
	}

	if size < 1 {
		size = 10
	}

	QDB := DB.Table("full_table").Select("full_table.*, token_ext.type, token_ext.return_type")
	CDB := DB.Table("full_table").Select("COUNT(full_table.id)")
	if date != nil && *date != "" {
		start, end, err := dateToRange(*date)
		if err != nil {
			return "", 0, err
		}

		sub := `
			INNER JOIN (
				SELECT chain, symbol, MAX(created_at) AS max_created_at
				FROM full_table
				WHERE created_at >= ? AND created_at <= ?
				GROUP BY chain, symbol
			) AS sub 
			ON full_table.chain = sub.chain 
			AND full_table.symbol = sub.symbol
			AND full_table.created_at = sub.max_created_at
		`

		QDB = QDB.InnerJoins(sub, start.Format("2006-01-02 15:04:05"), end.Format("2006-01-02 15:04:05"))
		CDB = CDB.InnerJoins(sub, start.Format("2006-01-02 15:04:05"), end.Format("2006-01-02 15:04:05"))
	} else {
		sub := `
			INNER JOIN (
				SELECT chain, symbol->'$.symbol' as symbol, MAX(created_at) AS max_created_at
				FROM full_table
				GROUP BY chain, symbol->'$.symbol'
			) AS sub 
			ON full_table.chain = sub.chain 
			AND full_table.symbol->'$.symbol' = sub.symbol 
			AND full_table.created_at = sub.max_created_at
		`
		QDB = QDB.InnerJoins(sub)
		CDB = CDB.InnerJoins(sub)
	}

	if chain != nil && *chain != "" {
		QDB = QDB.Where("full_table.chain = ?", *chain)
		CDB = CDB.Where("full_table.chain = ?", *chain)
	}

	if asset != nil && *asset != "" {
		QDB = QDB.Where("token_ext.type = ?", *asset)
		CDB = CDB.Where("token_ext.type = ?", *asset)
	}

	if returnType != nil && *returnType != "" {
		QDB = QDB.Where("token_ext.return_type = ?", *returnType)
		CDB = CDB.Where("token_ext.return_type = ?", *returnType)
	}

	if token != nil && *token != "" {
		QDB = QDB.Where("full_table.symbol->'$.symbol' LIKE CONCAT('%', ?, '%')", *token)
		CDB = CDB.Where("full_table.symbol->'$.symbol' LIKE CONCAT('%', ?, '%')", *token)
	}

	QDB = QDB.
		Joins("left join token_ext on full_table.symbol->'$.symbol'  = token_ext.token AND full_table.chain = token_ext.chain")
	CDB = CDB.
		Joins("left join token_ext on full_table.symbol->'$.symbol'  = token_ext.token AND full_table.chain = token_ext.chain")

	rows, err := QDB.Limit(size).Offset((page - 1) * size).Rows()
	if err != nil {
		return "", 0, err
	}

	ys := []FullTable{}
	for rows.Next() {
		var t FullTable
		if err := rows.Scan(
			&t.ID,
			&t.Source,
			&t.Chain,
			&t.BatchID,
			&t.Symbol,
			&t.FarmApy,
			&t.PoolApy,
			&t.Apy,
			&t.Tvl,
			&t.Volume,
			&t.Tx,
			&t.Price,
			&t.CreatedAt,
			&t.InsertedAt,
			&t.Type,
			&t.ReturnType,
		); err != nil {
			rows.Close()
			panic("解析数据失败: " + err.Error())
		}
		ys = append(ys, t)
	}
	rows.Close()

	var count int64
	result := CDB.Count(&count)
	if result.Error != nil {
		return "", 0, result.Error
	}

	jsonStr, err := json.Marshal(ys)
	if err != nil {
		return "", 0, err
	}
	return string(jsonStr), count, nil
}

func dateToRange(dateStr string) (time.Time, time.Time, error) {
	layout := "2006-01-02"
	startDate, err := time.Parse(layout, dateStr)
	if err != nil {
		return time.Time{}, time.Time{}, err
	}
	endDate := startDate.Add(24 * time.Hour)
	return startDate, endDate, nil
}

type FullTable struct {
	ID         int64      `gorm:"column:id;primaryKey;autoIncrement:true" json:"id"`
	Source     string     `gorm:"column:source;not null" json:"source"`
	Chain      string     `gorm:"column:chain;not null" json:"chain"`
	BatchID    *int64     `gorm:"column:batch_id" json:"batch_id"`
	Symbol     *string    `gorm:"column:symbol" json:"symbol"`
	FarmApy    *float64   `gorm:"column:farm_apy" json:"farm_apy"`
	PoolApy    *float64   `gorm:"column:pool_apy" json:"pool_apy"`
	Apy        *float64   `gorm:"column:apy" json:"apy"`
	Tvl        *float64   `gorm:"column:tvl" json:"tvl"`
	Volume     *float64   `gorm:"column:volume" json:"volume"`
	Tx         *int64     `gorm:"column:tx" json:"tx"`
	Price      *float64   `gorm:"column:price" json:"price"`
	Type       *string    `gorm:"column:type" json:"type"`
	ReturnType *string    `gorm:"column:return_type" json:"return_type"`
	CreatedAt  *time.Time `gorm:"column:created_at" json:"created_at"`
	InsertedAt *time.Time `gorm:"column:inserted_at;default:CURRENT_TIMESTAMP" json:"inserted_at"`
}
