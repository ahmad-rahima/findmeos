# fmos -- find me os
# This knowledge base system would ask the user number of questions
# to choose the best linux distro for the user depending in his answers.


import pprint
from experta import *


import csv

filename = "data.csv"

distros = {}

with open(filename, "r") as f:
    reader = csv.reader(f)
    headers = next(reader)

    for row in reader:
        key = row[0]
        values = {headers[i]: float(cell) for i, cell in enumerate(row[1:])}
        distros[key] = values   

# pprint.pprint(distros)


class Question(Fact):
    _0 = Field(str, mandatory=True)
    # _1 = Field(mandatory=True)


# Distro Properties
class Stability(Fact):
    pass

class Minimalism(Fact):
    pass

class OldHardwareSupport(Fact):
    pass

class HardwareSupport(Fact):
    pass 

class SnapshotSupport(Fact):
    pass 

class BackupSupport(Fact):
    pass

class ConfigInstallProcess(Fact):
    pass

class SimpleInstallProcess(Fact):
    pass 

class DefaultDesktopEnvironment(Fact):
    pass

class CommunityDesktopEnvironment(Fact):
    pass

class ChangingDesktopEnvironmentEase(Fact):
    pass

class Security(Fact):
    pass 

class Privacy(Fact):
    pass

class FOSS(Fact):
    pass

class GamingSupport(Fact):
    pass

class CommunitySize(Fact):
    pass 

class CommunityActivity(Fact):
    pass

class DefaultPackageManager(Fact):
    pass

class ReleaseCycle(Fact):
    pass

class LinuxExperience(Fact):
    pass

class Base(Fact):
    pass


class CommunityTarget(Fact):
    pass

class HardwareTarget(Fact):
    pass

class GamingTarget(Fact):
    pass

class LinuxBeforeTarget(Fact):
    pass

class DesktopTarget(Fact):
    pass

class StabilityTarget(Fact):
    pass

class MinimalismTarget(Fact):
    pass 

class SecurityPrivacyTarget(Fact):
    pass

class WindowsTarget(Fact):
    pass


class Target(Fact):
    _0 = Field(float, mandatory=True)
    distro = Field(str, mandatory=True)
    target = Field(str)

class OSChooser(KnowledgeEngine):

    @DefFacts()
    def init_distros(self):
        yield Question("How much do you care about the community of the distro?", "community", float)
        yield Question("How much do you care about the support of hardware? " 
                       "Meaning do you expect the distro to run on as much devices as possible?", 'hardware', float)
        # yield Question("Have you ever used linux before?", LinuxBeforeTarget, bool)
        yield Question("How much are you interested in gaming in linux?", 'gaming', float)
        yield Question("How much do you care about desktop experience out of box?", 'desktop', float)
        # yield Question("How much are you interseted into stability and rollback support of the distro?", StabilityTarget, float)
        yield Question("How much do you care about minimal linux experience?", 'minimalisim', float) # minimal && power_install
        yield Question("How much do you care about security and privacy of the distro?", 'security_privacy', float)
        yield Question("Do you consider running the distro along side windows?", 'windows', float) # dual_boot && secure_boot

    @Rule(
            AS.f1 << Target(MATCH.cf1, distro=MATCH.distro),
            AS.f2 << Target(MATCH.cf2, distro=MATCH.distro),
            TEST(lambda distro: distro != ''),
            TEST(lambda f1, f2: f1!=f2),
            TEST(lambda cf1: cf1>0),
            TEST(lambda cf2: cf2>0),
            salience=100
    )
    def combine_certainties_1(self,f1,f2,cf1,cf2):
        self.retract(f1)
        cf_=cf1+cf2*(1-cf1)
        self.modify(f2, _0=cf_)
               
    @Rule(
            AS.f1 << Target(MATCH.cf1, distro=MATCH.distro),
            AS.f2 << Target(MATCH.cf2, distro=MATCH.distro),
            TEST(lambda distro: distro != ''),
            TEST(lambda f1,f2: f1!=f2),
            TEST(lambda cf1: cf1<0),
            TEST(lambda cf2: cf2<0),
            salience = 100
    )
    def combine_certainties_2(self,f1,f2,cf1,cf2):
        self.retract(f1)
        cf_=cf1+cf2*(1+cf1)
        self.modify(f2, _0=cf_)
     
    @Rule(
            AS.f1 << Target(MATCH.cf1, distro=MATCH.distro),
            AS.f2 << Target(MATCH.cf2, distro=MATCH.distro),
            TEST(lambda distro: distro != ''),
            TEST(lambda f1,f2: f1!=f2),
            TEST(lambda cf1: cf1>0),
            TEST(lambda cf2: cf2<0),
            salience = 100
    )
    def combine_certainties_3(self,f1,f2,cf1,cf2):
        self.retract(f1)
        cf=min(abs(cf1),abs(cf2))
        try:
            cf_=(cf1+cf2)/(1-cf)
        except ZeroDivisionError:
            cf_=(cf1+cf2)/(1-0.05)
        self.modify(f2, _0=cf_)
    
    @Rule(
        AS.f << Target(MATCH.cf_rule, distro='', target="minimalisim")
    )
    def minimalisim_rule(self, f, cf_rule):
        for distro in distros:
            cf1 = 1 - distros[distro]['desktop_out_of_box']
            cf2 = distros[distro]['power_install_process']
            cf3 = distros[distro]['lightweight']
            cf = min(cf1, cf2, cf3)

            self.declare(Target(cf * cf_rule, distro=distro))

        self.retract(f)


    @Rule(
        AS.f << Target(MATCH.cf_rule, distro='', target="desktop")
    )
    def desktop_rule(self, f, cf_rule):
        for distro in distros:
            cf1 = distros[distro]['desktop_out_of_box']
            cf2 = distros[distro]['simplicity_install_process']
            cf3 = distros[distro]['stability']
            cf = min(cf1, cf2, cf3)

            self.declare(Target(cf * cf_rule, distro=distro))

        self.retract(f)

    @Rule(
        AS.f << Target(MATCH.cf_rule, distro='', target="windows")
    )
    def desktop_rule(self, f, cf_rule):
        for distro in distros:
            cf1 = distros[distro]['secure_boot']
            cf2 = 1 - distros[distro]['systemd_boot']
            cf = min(cf1, cf2)

            self.declare(Target(cf * cf_rule, distro=distro))

        self.retract(f)


    @Rule(
        AS.f << Target(MATCH.cf_rule, distro='', target="community")
    )
    def community_rule(self, f, cf_rule):
        for distro in distros:
            cf1 = distros[distro]['community_size']
            cf2 = distros[distro]['community_activity']
            cf = min(cf1, cf2)

            self.declare(Target(cf * cf_rule, distro=distro))

        self.retract(f)
            
    @Rule(
        AS.f << Target(MATCH.cf_rule, distro='', target="hardware")
    )
    def hardware_rule(self, f, cf_rule):
        for distro in distros:
            cf1 = distros[distro]['hardware_support']
            cf2 = distros[distro]['old_hardware_support']
            cf = min(cf1, cf2)

            self.declare(Target(cf * cf_rule, distro=distro))

        self.retract(f)

    @Rule(
            AS.f << Target(MATCH.cf_rule, distro='', target="privacy_security")
    )
    def security_privacy_rule(self, f, cf_rule):
        for distro in distros:
            cf1 = distros[distro]['security']
            cf2 = distros[distro]['privacy']
            cf = min(cf1, cf2)

            self.declare(Target(cf * cf_rule, distro=distro))

        self.retract(f)

    # @Rule(
    #         LinuxBeforeTarget(MATCH.cf_rule, distro=None)
    # )
    # def used_linux_before_rule(self, cf_rule):
    #     for distro in distros:
    #         cf = min(cf1, cf2)

    #         self.declare(HardwareTarget(cf * cf_rule, distro=distro))
      
    @Rule(
            AS.f << Target(MATCH.cf_rule, distro='', target="gaming")
    )
    def gaming_rule(self, f, cf_rule):
        for distro in distros:
            cf1 = distros[distro]['gaming_support']
            cf2 = distros[distro]['hardware_support']
            cf = min(cf1, cf2)

            self.declare(Target(cf * cf_rule, distro=distro))

        self.retract(f)
      

    @Rule(
          AS.f << Question(MATCH.q, MATCH.target, MATCH.t)
         )
    def ask_question(self, q, target, t):
        certainty = self.next_question(q, t) 
        print('-' * 60, end='\n')
        self.declare(Target(certainty, distro='', target=target))
   
    def next_question(self, q, ans_type):
        print(q,"\n")
        print("reply: ", end='')

        if ans_type == float:
            allowed_values = (-1, -0.5, 0, 0.5, 1)
            try:
                reply=float(input())
            except:
                reply=10000
            
            while reply not in allowed_values:
                print(q,"\n")
                print("reply: ", end='')
                try:
                    reply=float(input())
                except:reply=1000
                print("\n")
            return float(reply)

        else: 
            while True:
                ans = input()
                if ans.strip().lower() == 'y':
                    return True
                if ans.strip().lower() == 'n':
                    return False
                print("Wrong input (y/n)?\nreply: ", end='')
        

    
    # @Rule()
    # def ask_for_previous_experience():
    #     yield Question("Have you ever used linux before?", LinuxExperience, bool) 

    # def docker_or_real_machine_or_vm():
    #     # missing piece. take some data!
    #     yield Question("Where do you plan to use this distro on?", TargetMachine, str, 
    #                    ("real", "virtual", "container"))
        
    # def real_usage_or_exprimenting():
    #     yield Question("Do you plan to use this distro just for expirimentation?", Expirement, float)

    # def do_you_plan_to_dual_boot():
    #     yield Question("Do you plan to dual boot this distro?", DualBoot, float)

    # def do_you_plan_to_use_secure_boot():
    #     yield Question("Do you plan to use secure boot?", SecureBoot, float)
        
    # @Rule(LinuxExperience(v), TEST(lambda v: v > .5))
    # def what_base_distro_prefer():
    #     pass
        
    # def ask_for_user_level():
    #     pass

    # def how_secure():
    #     yield Question("How much do you care about security of the os?") # range 0..1
        
    # def how_private():
    #     yield Question("How much do you care about privacy of the os?") # range 0..1
        
    # def how_stable():
    #     yield Question("How much do you care about stability of the os?") # range 0..1
        
    # @Rule(LinuxExperience(v), TEST(lambda v: v > .5))
    # def how_comfortable_at_cli():
    #     yield Question("How comfortable are you at using the cli?")

    # @Rule(LinuxExperience(v), TEST(lambda v: v > .5))
    # def desktop_environment_preference():
    #     yield Has("desktop_environment_preference")

    # @Rule(LinuxExperience(v), TEST(lambda v: v < .5))
    # def desktop_environment_preference():
    #     yield HasNot("desktop_environment_preference")

    # def prefer_windows_or_mac_ui():
    #     # if windows; kde, cinnamon
    #     # if mac; gnome, elementry  
    #     pass

    # @DefFacts()
    # def init_package_manager():
    #     yield PackageManager("Debian", "apt")
    #     yield PackageManager("Fedora", "dnf")
    #     yield PackageManager("Arch", "pacman")
    #     yield PackageManager("Redhat", "yum")

    # @DefFacts()
    # def init_security():
    #     yield Security("Debian", 14)
    #     yield Security("Fedora", 20)
    #     yield Security("Arch", 11)

    # @DefFacts()
    # def init_release_cycle():
    #     yield ReleaseCycle("Debian", 2)
    #     yield ReleaseCycle("Arch", 0)
    #     yield ReleaseCycle("Fedora", .6)

    # @DefFacts()
    # def init_desktop_env():
    #     yield Desktop("Fedora", "GNOME")
    #     yield Desktop("Ubuntu", "GNOME")
        
    #     yield Spin("Fedora", "i3")

    # @DefFacts()
    # def init_installation_process():
    #     yield InstallationProcess("Ubuntu", 100)
    #     yield InstallationProcess("Mint", 100)
    #     yield InstallationProcess("Debian", 50)
    #     yield InstallationProcess("Fedora", 75)
    #     yield InstallationProcess("Arch", 0)

    # @DefFacts()
    # def init_base_distor():
    #     yield Base("Ubuntu", "Debian")
    #     yield Base("Debian", None)
    #     yield Base("Fedora", "Redhat")

    # @DefFacts()
    # def init_gnu_or_unix():
    #     yield PreferGNU("Fedora")
    #     yield PreferGNU("Arch")

    # @DefFacts()
    # def init_unix_base():
    #     yield UnixBase("Fedora", .3)
    #     yield UnixBase("Slackware", .9)

    # @DefFacts()
    # def init_community_driven():
    #     yield Community("Arch")
    #     yield Community("Nobara")


    # @DefFacts
    # def init_ease_of_use():
    #     yield EaseUse("Ubuntu", .8)
    #     yield EaseUse("Mint", 1)
    #     yield EaseUse("NixOS", .1)
    #     yield EaseUse("Debian", .5)

    # @DefFacts()
    # def init_compatiablity():
    #     pass

    # @DefFacts()
    # def init_focus():
    #     yield Focus("Ubuntu", None)
    #     yield Focus("Fedora", "Desktop")
    #     yield Focus("Debian", None)

    # @DefFacts()
    # def init_point_or_rolling_release():
    #     yield RollingRelease("Arch")
    #     yield RollingRelease("Gentoo")

    # @DefFacts()
    # def init_initsystem():
    #     yield InitSystem("Arch", "SystemD")
    #     yield InitSystem("Fedora", "SystemD")
    #     yield InitSystem("Gentoo", "not")

    # @DefFacts()
    # def init_licensing():
    #     yield Proprietary("Oracle")

    # @DefFacts()
    # def init():
    #     yield Question("What is your level of experience with Linux?")
    #     yield Question("What is your preferred desktop environment?")
    #     yield Question("Do you have a preference for the package manager?")
    #     yield Question("Do you require long-term support (LTS) for your distribution?")
    #     yield Question("Do you prefer a rolling-release or a fixed-release distribution?")

        

if __name__ == '__main__':
    engine = OSChooser()
    engine.reset()
    engine.run()
    print(engine.facts)