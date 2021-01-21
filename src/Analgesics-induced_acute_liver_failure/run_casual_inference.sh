ALBERT_OUTPUT=../../dat/Analgesics-induced_acute_liver_failure/output
DATA_DIR=../../dat/Analgesics-induced_acute_liver_failure
CAUSAL_OUTPUT_DIR=$DATA_DIR/causal_result

python causal_inference.py \
  --probability-file=$ALBERT_OUTPUT/test_results.tsv \
  --feature-file=$DATA_DIR/proc/feature.tsv \
  --out-dir=$CAUSAL_OUTPUT_DIR

