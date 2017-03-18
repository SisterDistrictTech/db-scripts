CREATE TABLE national_districts
	(id int(11) NOT NULL auto_increment primary key,
    state varchar(2) NOT NULL,
    district int(3),
    district_abbr varchar(6) NOT NULL,
    date_modified TIMESTAMP not null default current_timestamp(),
    user_modified varchar(20) not null
    );
    

DELIMITER ;;
CREATE TRIGGER `natl_dist_insert` BEFORE INSERT ON `national_districts` FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;


DELIMITER ;;
CREATE TRIGGER `natl_dist_update` BEFORE update ON `national_districts` FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;


create table raw_natl_district_data
	(id int(11) NOT NULL auto_increment primary key,
    date_added timestamp not null default current_timestamp(),
    user_added varchar(20) not null,
    district_id int(11) not null,
    election_year int(4) not null,
    raw_data text,
    foreign key fk_district_id(district_id) references national_districts(id));
    
delimiter ;;
create trigger raw_data_insert before insert on raw_natl_district_data for each row
begin
	set new.user_added = current_user();
end;;
delimiter ;

create table national_district_metrics
	(id int(11) not null auto_increment primary key,
    district_id int(11) not null,
    metric_type enum('Cook Code', 'Swing Left Index') not null,
    metric_value varchar(20),
    metric_date datetime,
	date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20),
    foreign key fk_district_id(district_id) references national_districts(id));
    
DELIMITER ;;
CREATE TRIGGER metrics_insert BEFORE INSERT ON national_district_metrics FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table national_district_races
	(id int(11) not null auto_increment primary key,
    district_id int(11) not null,
    election_year int(4) not null,
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20),
    rep_elect_name varchar(100),
    rep_elect_party enum('R', 'D', 'I', 'L'),
    uncontested boolean,
    percent_vote_winner float,
    losing_candidate varchar(100),
    percent_vote_loser float,
    num_vote_loser int(11),
    why_lost enum('A', 'B', 'C'),
    different_next_time text,
    swing_code enum('1', '2', '3', '4', '5'),
    voter_reg boolean,
    opportunity_1 text,
	opportunity_2 text,	
	opportunity_3 text,
	volunteers_used bool,
	volunteer_notes text,
    year_flipped int(4),
	flip_reason enum('A', 'B', 'C'),
    money_to_flip text,
	sw_margin float,
	sw_total_votes int(11),
	rnc_targeted bool,
    foreign key fk_district_id(district_id) references national_districts(id));
    
DELIMITER ;;
CREATE TRIGGER races_insert BEFORE INSERT ON national_district_races FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;


DELIMITER ;;
CREATE TRIGGER races_update BEFORE update ON national_district_races FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table issues
	(id int(11) NOT NULL auto_increment primary key,
    issue_name varchar(50) not null,
    issue_desc text,
	date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null
    );
    
DELIMITER ;;
CREATE TRIGGER issues_insert BEFORE INSERT ON issues FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;


DELIMITER ;;
CREATE TRIGGER issues_update BEFORE update ON issues FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table race_issues
	(race_id int(11) not null,
    issue_id int(11) not null,
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null,
    foreign key fk_race_id(race_id) references national_district_races(id),
    foreign key fk_issue_id(issue_id) references issues(id));
    
DELIMITER ;;
CREATE TRIGGER race_issues_insert BEFORE INSERT ON race_issues FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;


DELIMITER ;;
CREATE TRIGGER race_issues_update BEFORE update ON race_issues FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table race_expenditures
	(id int(11) NOT NULL auto_increment primary key,
    race_id int(11) not null,
    amount float,
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null,
    expenditure_date date,
    exp_position text,
    committee text,
    payee text,
    purpose text,
    description text,
    foreign key fk_race_id(race_id) references national_district_races(id));
    
DELIMITER ;;
CREATE TRIGGER expenditures_insert BEFORE INSERT ON race_expenditures FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;


DELIMITER ;;
CREATE TRIGGER expenditures_update BEFORE update ON race_expenditures FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table district_demo
	(id int(11) NOT NULL auto_increment primary key,
    source_year int(4) not null,
    district_id int(11) not null,
    demo_type enum('median_income', 'am_ind_pct', 'am_ind_18_pct', 'asian_pct', 'asian_18_pct', 'black_pct', 'black_18_pct', 'latinx_pct', 'latinx_18_pct', 'islander_pct', 'islander_18_pct', 'other_pct', 'other_18_pct', 'white_pct', 'white_18_pct', 'total_pop', 'unemployed_pct', 'pub_asst_pct', 'medicaid_exp_bool') not null, 
    demo_value float,
   	date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null,
    foreign key fk_district_id(district_id) references national_districts(id));
    
DELIMITER ;;
CREATE TRIGGER district_demo_insert BEFORE INSERT ON district_demo FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;


DELIMITER ;;
CREATE TRIGGER district_demo_update BEFORE update ON district_demo FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table industries
	(id int(11) NOT NULL auto_increment primary key,
    industry_name varchar(50),
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null);
    
DELIMITER ;;
CREATE TRIGGER industries_insert BEFORE INSERT ON industries FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;


DELIMITER ;;
CREATE TRIGGER industries_update BEFORE update ON industries FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table district_industry
	(district_demo_id int(11) not null,
    industry_id int(11) not null,
    rank int(2) not null,
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null,
    foreign key fk_dd_id(district_demo_id) references district_demo(id),
    foreign key fk_industry_id(industry_id) references industries(id));
    
DELIMITER ;;
CREATE TRIGGER district_industry_insert BEFORE INSERT ON district_industry FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;


DELIMITER ;;
CREATE TRIGGER district_industry_update BEFORE update ON district_industry FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table pres_races
	(id int(11) NOT NULL auto_increment primary key,
    race_year int(4) not null,
    dem_candidate varchar(100) not null,
    rep_candidate varchar(100) not null,
    winning_party enum('R', 'D', 'I', 'L') not null,
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null);
    
DELIMITER ;;
CREATE TRIGGER pres_races_insert BEFORE INSERT ON pres_races FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;


DELIMITER ;;
CREATE TRIGGER pres_races_update BEFORE update ON pres_races FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table pres_dist_voting
	(id int(11) NOT NULL auto_increment primary key,
	district_id int(11) not null,
    pres_race_id int(11) not null,
    voting_pct float,
    pres_dem_pct float,
    pres_rep_pct float,
    pres_dem_num float,
    pres_rep_num float,
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null,
    foreign key fk_district_id(district_id) references national_districts(id),
    foreign key fk_pres_race_id(pres_race_id) references pres_races(id));
    
DELIMITER ;;
CREATE TRIGGER pres_voting_insert BEFORE INSERT ON pres_dist_voting FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;

DELIMITER ;;
CREATE TRIGGER pres_voting_update BEFORE update ON pres_dist_voting FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table contact_types
	(id int(11) NOT NULL auto_increment primary key,
    contact_type varchar(50),
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null);
    
DELIMITER ;;
CREATE TRIGGER contact_types_insert BEFORE INSERT ON contact_types FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;

DELIMITER ;;
CREATE TRIGGER contact_types_update BEFORE update ON contact_types FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table contacts
	(id int(11) NOT NULL auto_increment primary key,
    contact_type_id int(11) not null,
    district_id int(11),
    state varchar(2),
    date_added timestamp not null,
    first_name varchar(20),
    last_name varchar(30),
    title varchar(50),
    org_name varchar(50),
    sd_contact_name varchar(50),
    sd_contact_email varchar(50),
    notes text,
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null,
    foreign key fk_type_id(contact_type_id) references contact_types(id));
    
DELIMITER ;;
CREATE TRIGGER contacts_insert BEFORE INSERT ON contacts FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;

DELIMITER ;;
CREATE TRIGGER contacts_update BEFORE update ON contacts FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table contact_addresses
	(id int(11) NOT NULL auto_increment primary key,
    contact_id int(11) not null,
    email varchar(50),
    phone varchar(15),
    address varchar(255),
    url varchar(255),
    facebook varchar(100),
    twitter varchar(30),
	date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null,
    foreign key fk_contact_id(contact_id) references contacts(id));
    
DELIMITER ;;
CREATE TRIGGER contact_addresses_insert BEFORE INSERT ON contact_addresses FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;

DELIMITER ;;
CREATE TRIGGER contact_addresses_update BEFORE update ON contact_addresses FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table sources
	(id int(11) NOT NULL auto_increment primary key,
    url varchar(255),
    description text,
    state varchar(2),
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) not null);
    
DELIMITER ;;
CREATE TRIGGER sources_insert BEFORE INSERT ON sources FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;

DELIMITER ;;
CREATE TRIGGER sources_update BEFORE update ON sources FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
create table voting_rights
	(id int(11) NOT NULL auto_increment primary key,
    state varchar(2) not null,
    data_year int(4) not null,
    voter_id_law bool not null,
    type_of_law text,
    forms_of_id text,
    voting_notes text,
    pending_leg text,
    date_modified timestamp not null default current_timestamp(),
    user_modified varchar(20) default null);
    
DELIMITER ;;
CREATE TRIGGER voting_rights_insert BEFORE INSERT ON voting_rights FOR EACH ROW
BEGIN
    set new.user_modified = current_user();
END;;
DELIMITER ;

DELIMITER ;;
CREATE TRIGGER voting_rights_update BEFORE update ON voting_rights FOR EACH ROW
BEGIN
    SET NEW.date_modified = NOW();
    set new.user_modified = current_user();
END;;
DELIMITER ;
    
