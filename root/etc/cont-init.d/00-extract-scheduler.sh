#!/usr/bin/with-contenv sh

if [ -d "${SCHEDULER_VOLUME}/script.d" ]; then
  for SCRIPT in ${SCHEDULER_VOLUME}/script.d/*
	do
		if [ -f $SCRIPT ]
		then
			sh $SCRIPT
		fi
	done
fi
