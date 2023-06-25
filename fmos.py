# fmos -- find me os
# This knowledge base system would ask the user number of questions
# to choose the best linux distro for the user depending in his answers.


from experta import *


class Question(Fact):
    _0 = Field(str, mandatory=True)
    _1 = Field(mandatory=True)



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


# user choices
class Prefered(Fact):
    pass

class Must(Fact):
    pass

class MustNot(Fact):
    pass 

class PreferedNot(Fact):
    pass

class Irrelevant(Fact):
    pass


# Ubuntu(PackageManager("apt"), ReleaseCycle("9"), DefaultDesktopEnviroment("GNOME"), ...)
# Prefered(PackageManager("dnf"), ReleaseCycle("9"))
# Must(PackageManager("dnf"), ReleaseCycle("6"))
# MustNot(PackageManager("dnf"), ReleaseCycle("6"))
# PreferedNot(PackageManager("dnf"), ReleaseCycle("9"))
# Ignostic(PackageManager("dnf"))
# Irrelevant()


class Ubuntu(Fact):
    pass


class OSChooser(KnowledgeEngine):


    @DefFacts()
    def init_distros():
        yield Ubuntu(DefaultPackageManager("apt"), Base("Debian"), ReleaseCycle(9), Security(.8), Privacy(.8), Minimalism(.2))
        yield Fedora(DefaultPackageManager("dnf"), Base("Redhat"), ReleaseCycle(6), Security(.9), Privacy(.9))

        # yield Prefered(DefaultPackageManager("apt"), Base("Debian"))
        # yield MustNot(ReleaseCycle(None)) # rolling release
        
    
    @Rule()
    def ask_for_previous_experience():
        yield Question("Have you ever used linux before?", LinuxExperience, bool) 

    def docker_or_real_machine_or_vm():
        # missing piece. take some data!
        yield Question("Where do you plan to use this distro on?", TargetMachine, str, 
                       ("real", "virtual", "container"))
        
    def real_usage_or_exprimenting():
        yield Question("Do you plan to use this distro just for expirimentation?", Expirement, float)

    def do_you_plan_to_dual_boot():
        yield Question("Do you plan to dual boot this distro?", DualBoot, float)

    def do_you_plan_to_use_secure_boot():
        yield Question("Do you plan to use secure boot?", SecureBoot, float)
        
    @Rule(LinuxExperience(v), TEST(lambda v: v > .5))
    def what_base_distro_prefer():
        pass
        
    def ask_for_user_level():
        pass

    def how_secure():
        yield Question("How much do you care about security of the os?") # range 0..1
        
    def how_private():
        yield Question("How much do you care about privacy of the os?") # range 0..1
        
    def how_stable():
        yield Question("How much do you care about stability of the os?") # range 0..1
        
    @Rule(LinuxExperience(v), TEST(lambda v: v > .5))
    def how_comfortable_at_cli():
        yield Question("How comfortable are you at using the cli?")

    @Rule(LinuxExperience(v), TEST(lambda v: v > .5))
    def desktop_environment_preference():
        yield Has("desktop_environment_preference")

    @Rule(LinuxExperience(v), TEST(lambda v: v < .5))
    def desktop_environment_preference():
        yield HasNot("desktop_environment_preference")

    def prefer_windows_or_mac_ui():
        # if windows; kde, cinnamon
        # if mac; gnome, elementry  
        pass

    @DefFacts()
    def init_package_manager():
        yield PackageManager("Debian", "apt")
        yield PackageManager("Fedora", "dnf")
        yield PackageManager("Arch", "pacman")
        yield PackageManager("Redhat", "yum")

    @DefFacts()
    def init_security():
        yield Security("Debian", 14)
        yield Security("Fedora", 20)
        yield Security("Arch", 11)

    @DefFacts()
    def init_release_cycle():
        yield ReleaseCycle("Debian", 2)
        yield ReleaseCycle("Arch", 0)
        yield ReleaseCycle("Fedora", .6)

    @DefFacts()
    def init_desktop_env():
        yield Desktop("Fedora", "GNOME")
        yield Desktop("Ubuntu", "GNOME")
        
        yield Spin("Fedora", "i3")

    @DefFacts()
    def init_installation_process():
        yield InstallationProcess("Ubuntu", 100)
        yield InstallationProcess("Mint", 100)
        yield InstallationProcess("Debian", 50)
        yield InstallationProcess("Fedora", 75)
        yield InstallationProcess("Arch", 0)

    @DefFacts()
    def init_base_distor():
        yield Base("Ubuntu", "Debian")
        yield Base("Debian", None)
        yield Base("Fedora", "Redhat")

    @DefFacts()
    def init_gnu_or_unix():
        yield PreferGNU("Fedora")
        yield PreferGNU("Arch")

    @DefFacts()
    def init_unix_base():
        yield UnixBase("Fedora", .3)
        yield UnixBase("Slackware", .9)

    @DefFacts()
    def init_community_driven():
        yield Community("Arch")
        yield Community("Nobara")


    @DefFacts
    def init_ease_of_use():
        yield EaseUse("Ubuntu", .8)
        yield EaseUse("Mint", 1)
        yield EaseUse("NixOS", .1)
        yield EaseUse("Debian", .5)

    @DefFacts()
    def init_compatiablity():
        pass

    @DefFacts()
    def init_focus():
        yield Focus("Ubuntu", None)
        yield Focus("Fedora", "Desktop")
        yield Focus("Debian", None)

    @DefFacts()
    def init_point_or_rolling_release():
        yield RollingRelease("Arch")
        yield RollingRelease("Gentoo")

    @DefFacts()
    def init_initsystem():
        yield InitSystem("Arch", "SystemD")
        yield InitSystem("Fedora", "SystemD")
        yield InitSystem("Gentoo", "not")

    @DefFacts()
    def init_licensing():
        yield Proprietary("Oracle")

    @DefFacts()
    def init():
        yield Question("What is your level of experience with Linux?")
        yield Question("What is your preferred desktop environment?")
        yield Question("Do you have a preference for the package manager?")
        yield Question("Do you require long-term support (LTS) for your distribution?")
        yield Question("Do you prefer a rolling-release or a fixed-release distribution?")


        