#!/bin/bash

SCRIPTDIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

cd "$SCRIPTDIR"

rm -rf "./output"
mkdir -p "./output"

find "./input/" -type f -name '*.pdb' \
| ../voronota-js-voroif-gnn-v2 \
  --conda-path "${HOME}/miniconda3" --conda-env "voroif-gnn-v2-env" \
> "./output/results_using_gnn_set1_basic.txt"

find "./input/" -type f -name '*.pdb' \
| ../voronota-js-voroif-gnn-v2 \
  --conda-path "${HOME}/miniconda3" --conda-env "voroif-gnn-v2-env" \
  --run-faspr "${HOME}/git/ftdmp/core/FASPR_data/dun2010bbdep.bin" \
> "./output/results_using_gnn_set1_after_running_faspr.txt"

find "./input/" -type f -name '*.pdb' \
| ../voronota-js-voroif-gnn-v2 \
  --conda-path "${HOME}/miniconda3" --conda-env "voroif-gnn-v2-env" \
  --restrict-input '[-rnum 27:159]' \
> "./output/results_using_gnn_set1_after_restricting_input.txt"

find "./input/" -type f -name '*.pdb' \
| ../voronota-js-voroif-gnn-v2 \
  --conda-path "${HOME}/miniconda3" --conda-env "voroif-gnn-v2-env" \
  --restrict-input '[-rnum 27:159]' \
  --run-faspr "${HOME}/git/ftdmp/core/FASPR_data/dun2010bbdep.bin" \
> "./output/results_using_gnn_set1_after_restricting_input_and_running_faspr.txt"


find "./input/" -type f -name '*.pdb' \
| ../voronota-js-voroif-gnn-v2 \
  --conda-path "${HOME}/miniconda3" --conda-env "voroif-gnn-v2-env" \
  --gnn-models-dir "${SCRIPTDIR}/../trained_gnn_models" \
> "./output/results_using_gnn_set1_and_set2_basic.txt"

find "./input/" -type f -name '*.pdb' \
| ../voronota-js-voroif-gnn-v2 \
  --conda-path "${HOME}/miniconda3" --conda-env "voroif-gnn-v2-env" \
  --gnn-models-dir "${SCRIPTDIR}/../trained_gnn_models" \
  --run-faspr "${HOME}/git/ftdmp/core/FASPR_data/dun2010bbdep.bin" \
> "./output/results_using_gnn_set1_and_set2_after_running_faspr.txt"

find "./input/" -type f -name '*.pdb' \
| ../voronota-js-voroif-gnn-v2 \
  --conda-path "${HOME}/miniconda3" --conda-env "voroif-gnn-v2-env" \
  --gnn-models-dir "${SCRIPTDIR}/../trained_gnn_models" \
  --restrict-input '[-rnum 27:159]' \
> "./output/results_using_gnn_set1_and_set2_after_restricting_input.txt"

find "./input/" -type f -name '*.pdb' \
| ../voronota-js-voroif-gnn-v2 \
  --conda-path "${HOME}/miniconda3" --conda-env "voroif-gnn-v2-env" \
  --gnn-models-dir "${SCRIPTDIR}/../trained_gnn_models" \
  --restrict-input '[-rnum 27:159]' \
  --run-faspr "${HOME}/git/ftdmp/core/FASPR_data/dun2010bbdep.bin" \
> "./output/results_using_gnn_set1_and_set2_after_restricting_input_and_running_faspr.txt"


find "./output/" -type f -name '*.txt' \
| sort \
| while read -r RESULTFILE
do
	echo "$RESULTFILE"
	cat "$RESULTFILE" | sed 's/^/    /'
	echo
done

