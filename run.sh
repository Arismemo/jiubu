CURRENT_DIR=$( cd "$(dirname "$0")"; pwd)
echo $CURRENT_DIR
streamlit run web_front/扫码识别.py $CURRENT_DIR

