
from rlcard.envs.registration import register

register(
    env_id='shed',
    entry_point='shed.env.shed:ShedEnv',
)

import rlcard
rlcard.make('shed')