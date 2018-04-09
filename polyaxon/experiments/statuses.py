from jobs.statuses import JobLifeCycle
from libs.constants import UNKNOWN
from libs.statuses import BaseStatuses


class ExperimentLifeCycle(BaseStatuses):
    """Experiment lifecycle

    Props:
        * CREATED: created and waiting to be scheduled
        * BUILDING: started building imagesif necessary
        * SCHEDULED: scheduled waiting to be picked
        * STARTING: picked and is starting (jobs are created/building/pending)
        * RUNNING: one or all jobs is still running
        * SUCCEEDED: master and workers have finished successfully
        * FAILED: one of the jobs has failed
        * STOPPED: was stopped/deleted/killed
        * UNKNOWN: unknown state
    """
    CREATED = 'Created'
    BUILDING = 'Building'
    SCHEDULED = 'Scheduled'
    STARTING = 'Starting'
    RUNNING = 'Running'
    SUCCEEDED = 'Succeeded'
    FAILED = 'Failed'
    STOPPED = 'Stopped'
    UNKNOWN = UNKNOWN

    CHOICES = (
        (CREATED, CREATED),
        (BUILDING, BUILDING),
        (SCHEDULED, SCHEDULED),
        (STARTING, STARTING),
        (RUNNING, RUNNING),
        (SUCCEEDED, SUCCEEDED),
        (FAILED, FAILED),
        (STOPPED, STOPPED),
        (UNKNOWN, UNKNOWN),
    )

    VALUES = {
        CREATED, BUILDING, SCHEDULED, STARTING, RUNNING, SUCCEEDED, FAILED, STOPPED, UNKNOWN
    }

    RUNNING_STATUS = [SCHEDULED, BUILDING, STARTING, RUNNING]
    DONE_STATUS = [FAILED, STOPPED, SUCCEEDED]
    FAILED_STATUS = [FAILED]

    TRANSITION_MATRIX = {
        CREATED: {None, },
        BUILDING: {CREATED, },
        SCHEDULED: {CREATED, BUILDING, },
        STARTING: {SCHEDULED, },
        RUNNING: {SCHEDULED, STARTING, UNKNOWN},
        SUCCEEDED: {SCHEDULED, STARTING, RUNNING, UNKNOWN, },
        FAILED: {CREATED, SCHEDULED, SCHEDULED, STARTING, RUNNING, UNKNOWN, },
        STOPPED: set(VALUES),
    }

    @staticmethod
    def jobs_starting(job_statuses):
        return any([True if JobLifeCycle.is_starting(job_status) else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_running(job_statuses):
        return any([True if JobLifeCycle.is_running(job_status) else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_succeeded(job_statuses):
        return all([True if job_status == JobLifeCycle.SUCCEEDED else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_failed(job_statuses):
        return any([True if job_status == JobLifeCycle.FAILED else False
                    for job_status in job_statuses])

    @staticmethod
    def jobs_stopped(job_statuses):
        return any([True if job_status == JobLifeCycle.STOPPED else False
                    for job_status in job_statuses])

    @classmethod
    def jobs_unknown(cls, job_statuses):
        return any([True if job_status == JobLifeCycle.UNKNOWN else False
                    for job_status in job_statuses])

    @classmethod
    def jobs_status(cls, job_statuses):
        if not job_statuses:
            return None

        if cls.jobs_unknown(job_statuses):
            return cls.UNKNOWN

        if cls.jobs_stopped(job_statuses):
            return cls.STOPPED

        if cls.jobs_succeeded(job_statuses):
            return cls.SUCCEEDED

        if cls.jobs_failed(job_statuses):
            return cls.FAILED

        if cls.jobs_starting(job_statuses):
            return cls.STARTING

        if cls.jobs_running(job_statuses):
            return cls.RUNNING

        return cls.UNKNOWN
