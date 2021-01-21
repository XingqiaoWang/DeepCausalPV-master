ALBERT_OUTPUT=../../dat/Tramadol-related_mortalities/output
DATA_DIR=../../dat/Tramadol-related_mortalities
CAUSAL_OUTPUT_DIR=$DATA_DIR/causal_result

python causal_inference.py \
  --probability-file=$ALBERT_OUTPUT/test_results.tsv \
  --feature-file=$DATA_DIR/proc/feature.tsv \
  --out-dir=$CAUSAL_OUTPUT_DIR

