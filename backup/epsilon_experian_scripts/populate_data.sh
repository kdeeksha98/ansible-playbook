#!/bin/bash

POSTGRES_DATABASE='demographics'
POSTGRES_HOST='localhost'
POSTGRES_PASSWORD='alpha'
POSTGRES_PORT='5432'
POSTGRES_USERNAME='minion'
export PGPASSWORD="$POSTGRES_PASSWORD"

#DUMP file path
file_path_epsilon="/home/yashas/adcuratio/core-backend/demographics.csv"
file_path_experian="/home/yashas/adcuratio/core-backend/experian.csv"


#should be same as in create_table.sql file
epsilon_table_name="demographics"
experian_table_name="experian"


# CREATE TABLE
sql='\i create_epsilon_table.sql'
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

sql='\i create_experian_table.sql'
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"


#INSERT DATA
sql="\copy $epsilon_table_name(epsilon_id,INDV_ID,children_age_0_to_2_enhanced,children_age_3_to_5_enhanced,children_age_6_to_10_enhanced,children_age_11_to_15_enhanced,children_age_16_to_17_enhanced,advantage_household_education,advantage_household_education_indicator,household_type_family_composition_enhanced,advantage_household_marital_status,advantage_household_marital_status_indicator,advantage_individual_marital_status,advantage_individual_marital_status_indicator,advantage_home_owner,advantage_home_owner_indicator,advantage_individual_age,advantage_individual_age_indicator,occupation,ethnic_groups_codes,assimilation_code,advantage_target_narrow_band_income_3_0,target_net_worth_3_0,credit_active,number_of_vehicles_in_household,vehicle_make_1,vehicle_make_2,vehicle_make_3,vehicle_make_4,vehicle_make_5,vehicle_make_6,vehicle_model_1,vehicle_model_2,vehicle_model_3,vehicle_model_4,vehicle_model_5,vehicle_model_6,vehicle_year_1,vehicle_year_2,vehicle_year_3,vehicle_year_4,vehicle_year_5,vehicle_year_6,mt_brand_loyalists,mt_whats_on_sale_shoppers,mt_socially_active_on_facebook,sports_cycling_all,mt_amazon_prime_customers,niches_5_0,shopping_styles,music_any_all,mail_order_health_and_beauty_products_all,sports_sports_participation_all,sports_boating_sailing_all,sports_camping_hiking_all,sports_fishing_all,sports_fitness_exercise_all,sports_golf_all,sports_hunting_shooting_all,sports_hunting_big_game_all,sports_nascar_all,sports_running_jogging_all,sports_skiing_snowboarding_all,sports_walking_for_health_all,sports_yoga_pilates_all,data_provider_bv,operator_bv,bit_vector,operator_id,adcuratio_id,operator_shard_id,adcuratio_household_id) FROM $file_path_epsilon DELIMITER ',' CSV"
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

sql="\copy $experian_table_name(epsilon_id,matchlevel,alternate_fuel_electric,alternate_fuel_hybrid,buy_new,buy_used,price_20k_30k,price_30k_plus,price_30k_40k,price_40k_50k,price_50k_75k,price_75k_plus,alternate_fuel_car,car_any_model,cuv,suv,truck,luxury_car,luxury_cuv,luxury_suv,new_car,children_gender_0_3,children_gender_10_12,children_gender_13_15,children_gender_16_18,children_gender_4_6,children_gender_7_9,children_gender_0_1,education,gender,occupation_group,marital_status,household_income_range,age,home_owner,renter,last_12_months,last_6_months,new_parent,digital_savvy_dads,digital_savvy_moms,waistband_size,hunting_enthusisat,amusement_park,arts_and_crafts,attends_education_programs,avid_runner,boating_enthusisat,canoeing_and_kayaking_enthusisat,casino_gambling_enthusiast,cat_owner,coffee_connoisseur,dog_owner,do_it_yourselfer_enthusiast,family,fast_food,fishing_enthusisat,fitness_enthusiast,gourmet_cooking,healthy_living_enthusiast,home_improvement_spender,mlb,music_streaming,nascar_enthusiast,nba,nfl,nhl,on_a_diet,outdoor_enthusisat,pet_enthusiast,pga_tour,plays_golf,plays_hockey,plays_soccer,plays_tennis,snow_sports,sports_enthusiast,sweepstakes_and_lottery,video_gamer,weight_conscious,wine_lover,coupon_user,high_end_spirit_drinker,imported_beer_enthusiast,laptop_owner,loyalty_card_user,luxury_home_goods_shopper,luxury_store_shopper,non_prestige_makeup_brand,prestige_makeup_user,security_system_owner,supercenter_shoppers,tablet_owner,warehouse_club_member,volunteers,charities,credit_card_user_type,debit_card_user,major_credit_card_user,premium_credit_card_user,store_credit_card_user,gardening_enthusaist,active_investor,brokerage_account_owner,has_retirement_plan,mutual_fund_investor,participates_in_online_trading,frequent_flyer_program,has_grandchildren,business_travel_high_frequency,high_frequency_cruise_enthusiast,domestic_vacationer_high_frequency,foreign_vacationer_high_frequency,hotel_guest_loyality_program,life_insurance_policy,medical_insurance_policy_holders,medicare_policy_holder,active_declared,inactive_declared,green_aware_household,auto_part_store_shoppers,baby_registry_shoppers,big_box_shoppers,black_friday_shoppers,coffee_shop_visitor,college_sports_venues,concert_venues_visitors,easter_shoppers,electronics_store_shoppers,fathers_day_shoppers,financial_service_visitors,frequent_gym_goers,hardwood_floor_shoppers,high_end_furniture_shoppers,holiday_deal_shoppers,jewelery_store_shoppers,july_4th_shoppers,july_4th_travelers,lux_womens_retail_shoppers,mall_shoppers,mattress_store_shoppers,memorial_day_shoppers,mid_low_furniture_shoppers,mothers_day_shoppers,movie_theatre_visitors,outdoor_retail_shoppers,outlet_malls_shoppers,quick_service_restaurants_visitors,shoe_shoppers,sporting_goods_shoppers,summer_break_travelers,theme_park_visitors,valentines_day_shoppers,wedding_registry_shoppers,womens_retail_shoppers,young_women_retail_shoppers,cruiser_motorcycle_owner,touring_motorcycle_owner,accessories,apparel,computers,electronic_and_gadgets,food_and_beverage,furniture,general_and_miscellaneous,hobbies_and_entertainment,home_decor,home_maintenance,home_office,home_domestic,kitchen,lawn_and_garden,outdoor_living,outdoor_hard_goods,outdoor_soft_goods,personal_health,pets,seasonal_products,shoes,tabletop_and_dining,tools_and_automotive,toys,travel,engaged,new_job,expecting_baby,black_friday_shopper,mdl_non_traditional,mdl_fitness_device,food_based_subscriptions,apparel_based_subscriptions,cosmatic_based_subscriptions,prefer_gorcery_delivery,workout_at_home,plus_65_environmental_conscious,business_travel_score,family_order_kids,younger_kids,financial_advice,generation_b,generation_m,generaion_x,generation_z,influenced_by_environmental_changes,construction_recency,education_recency,government_recency,quick_service_restaurants,reatil_apparel,small_business,social_services,travel_recency,essential_workers,retired,single_adult,streaming_tv,brand_loyalists,deal_seekers,in_the_moment_shoppers,mainstream_adopters,novelty_seekers,organic_and_natural,quality_matters,recreational_shoppers,trendsetters,online_deal_voucher,discount_supercenters,ebid_sites,mid_high_end_store,specialty_dept_store,specialty_or_boutique,wholesale,mosaic_global_household,state_code,zip_code,data_provider_bv,operator_bv,experian_bit_vector,behaviour_bit_vector,children_bit_vector,bv_cons_behaviour,mosaic_code_bit_vector,state_code_bit_vector,bv_lifestyle_lm,bv_lifestyle,bv_true_touch,bv_social_media,bv_hh_consumer,bv_online_sub,adcuratio_id,operator_shard_id,adcuratio_household_id) FROM $file_path_experian DELIMITER ',' CSV"
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"


# ADD INDEX ON operator_shard_id COULMN
sql="CREATE UNIQUE INDEX refresh_operator_shard_id_uindex_epsilon ON $epsilon_table_name USING btree (operator_shard_id)"
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

sql="CREATE UNIQUE INDEX refresh_operator_shard_id_uindex_experian ON $experian_table_name USING btree (operator_shard_id)"
psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

echo "***adcuratio operator_shard_id column added***"

# # ADD adcuratio_houslehold_id COULUMN
# sql="ALTER TABLE $epsilon_table_name ADD COLUMN adcuratio_household_id integer"
# psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

# sql="ALTER TABLE $experian_table_name ADD COLUMN adcuratio_household_id integer"
# psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

# echo "***populating adcuratio household ID***"



# #Populate adcuratio_household_id
# sql="UPDATE $epsilon_table_name as d
#     SET
#         adcuratio_household_id=sq.adc
#     FROM
#         (SELECT epsilon_id, MIN(adcuratio_id) AS adc FROM $epsilon_table_name GROUP BY epsilon_id) AS sq
#     WHERE
#         d.epsilon_id = sq.epsilon_id;";
# psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

# sql="UPDATE $experian_table_name as d
#     SET
#         adcuratio_household_id=sq.adc
#     FROM
#         (SELECT epsilon_id, MIN(adcuratio_id) AS adc FROM $experian_table_name GROUP BY epsilon_id) AS sq
#     WHERE
#         d.epsilon_id = sq.epsilon_id;";
# psql -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -d "$POSTGRES_DATABASE" -U "$POSTGRES_USERNAME" -c "$sql"

echo "DONE!!!!!!!!!"
