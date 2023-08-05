#!/bin/bash -xe

DEST=$BASE/new
DEVSTACK_DIR=$DEST/devstack
source $DEVSTACK_DIR/openrc admin admin
unset OS_REGION_NAME

echo "Start to run single gateway topology test"
python run_yaml_test.py single_gw_topology_test.yaml "$OS_AUTH_URL" "$OS_TENANT_NAME" "$OS_USERNAME" "$OS_PASSWORD" "$OS_PROJECT_DOMAIN_ID" "$OS_USER_DOMAIN_ID"
if [ $? != 0 ]; then
    die $LINENO "Smoke test fails, error in single gateway topology test"
fi
echo "Start to run multi gateway topology test"
python run_yaml_test.py multi_gw_topology_test.yaml "$OS_AUTH_URL" "$OS_TENANT_NAME" "$OS_USERNAME" "$OS_PASSWORD" "$OS_PROJECT_DOMAIN_ID" "$OS_USER_DOMAIN_ID"
if [ $? != 0 ]; then
    die $LINENO "Smoke test fails, error in multi gateway topology test"
fi
echo "Start to run trunk test"
python run_yaml_test.py trunk_test.yaml "$OS_AUTH_URL" "$OS_TENANT_NAME" "$OS_USERNAME" "$OS_PASSWORD" "$OS_PROJECT_DOMAIN_ID" "$OS_USER_DOMAIN_ID"
if [ $? != 0 ]; then
    die $LINENO "Smoke test fails, error in trunk test"
fi
#echo "Start to run service function chain test"
#python run_yaml_test.py sfc_test.yaml "$OS_AUTH_URL" "$OS_TENANT_NAME" "$OS_USERNAME" "$OS_PASSWORD"
#if [ $? != 0 ]; then
#    die $LINENO "Smoke test fails, error in service function chain test"
#fi
echo "Start to run qos policy function test"
python run_yaml_test.py qos_policy_rule_test.yaml "$OS_AUTH_URL" "$OS_TENANT_NAME" "$OS_USERNAME" "$OS_PASSWORD" "$OS_PROJECT_DOMAIN_ID" "$OS_USER_DOMAIN_ID"
if [ $? != 0 ]; then
    die $LINENO "Smoke test fails, error in service function chain test"
fi
