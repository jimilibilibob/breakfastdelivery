mkdir ~/$1
cp ~/breakfastdelivery/kubernetes/aks/values.yaml ~/$1/values.yaml
sed -i 's/REPLACE/$1/g' ~/$1/values.yaml